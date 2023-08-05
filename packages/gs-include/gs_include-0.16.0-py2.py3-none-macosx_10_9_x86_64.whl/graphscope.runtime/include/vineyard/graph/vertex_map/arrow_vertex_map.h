/** Copyright 2020-2021 Alibaba Group Holding Limited.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
*/

#ifndef MODULES_GRAPH_VERTEX_MAP_ARROW_VERTEX_MAP_H_
#define MODULES_GRAPH_VERTEX_MAP_ARROW_VERTEX_MAP_H_

#include <algorithm>
#include <atomic>
#include <map>
#include <memory>
#include <mutex>
#include <string>
#include <thread>
#include <vector>

#include "basic/ds/array.h"
#include "basic/ds/arrow.h"
#include "basic/ds/hashmap.h"
#include "client/client.h"
#include "common/util/functions.h"
#include "common/util/typename.h"

#include "graph/fragment/property_graph_types.h"
#include "graph/fragment/property_graph_utils.h"
#include "graph/utils/thread_group.h"

namespace gs {

template <typename OID_T, typename VID_T>
class ArrowProjectedVertexMap;

}  // namespace gs

namespace vineyard {

template <typename OID_T, typename VID_T>
class ArrowVertexMapBuilder;

template <typename OID_T, typename VID_T>
class ArrowVertexMap
    : public vineyard::Registered<ArrowVertexMap<OID_T, VID_T>> {
  using oid_t = OID_T;
  using vid_t = VID_T;
  using label_id_t = property_graph_types::LABEL_ID_TYPE;
  using oid_array_t = typename vineyard::ConvertToArrowType<oid_t>::ArrayType;

 public:
  ArrowVertexMap() {}
  ~ArrowVertexMap() {}

  static std::unique_ptr<vineyard::Object> Create() __attribute__((used)) {
    return std::static_pointer_cast<vineyard::Object>(
        std::unique_ptr<ArrowVertexMap<OID_T, VID_T>>{
            new ArrowVertexMap<OID_T, VID_T>()});
  }

  void Construct(const vineyard::ObjectMeta& meta) {
    this->meta_ = meta;
    this->id_ = meta.GetId();

    this->fnum_ = meta.GetKeyValue<fid_t>("fnum");
    this->label_num_ = meta.GetKeyValue<label_id_t>("label_num");

    id_parser_.Init(fnum_, label_num_);

    o2g_.resize(fnum_);
    oid_arrays_.resize(fnum_);
    for (fid_t i = 0; i < fnum_; ++i) {
      o2g_[i].resize(label_num_);
      oid_arrays_[i].resize(label_num_);
      for (label_id_t j = 0; j < label_num_; ++j) {
        o2g_[i][j].Construct(meta.GetMemberMeta("o2g_" + std::to_string(i) +
                                                "_" + std::to_string(j)));

        typename InternalType<oid_t>::vineyard_array_type array;
        array.Construct(meta.GetMemberMeta("oid_arrays_" + std::to_string(i) +
                                           "_" + std::to_string(j)));
        oid_arrays_[i][j] = array.GetArray();
      }
    }
  }

  bool GetOid(vid_t gid, oid_t& oid) const {
    fid_t fid = id_parser_.GetFid(gid);
    label_id_t label = id_parser_.GetLabelId(gid);
    int64_t offset = id_parser_.GetOffset(gid);
    if (fid < fnum_ && label < label_num_ && label >= 0) {
      auto array = oid_arrays_[fid][label];
      if (offset < array->length()) {
        oid = array->GetView(offset);
        return true;
      }
    }
    return false;
  }

  bool GetGid(fid_t fid, label_id_t label_id, oid_t oid, vid_t& gid) const {
    auto iter = o2g_[fid][label_id].find(oid);
    if (iter != o2g_[fid][label_id].end()) {
      gid = iter->second;
      return true;
    }
    return false;
  }

  bool GetGid(label_id_t label_id, oid_t oid, vid_t& gid) const {
    for (fid_t i = 0; i < fnum_; ++i) {
      if (GetGid(i, label_id, oid, gid)) {
        return true;
      }
    }
    return false;
  }

  std::vector<oid_t> GetOids(fid_t fid, label_id_t label_id) {
    auto array = oid_arrays_[fid][label_id];
    std::vector<oid_t> oids;

    oids.resize(array->length());
    for (auto i = 0; i < array->length(); i++) {
      oids[i] = array->GetView(i);
    }

    return oids;
  }

  std::shared_ptr<oid_array_t> GetOidArray(fid_t fid, label_id_t label_id) {
    return oid_arrays_[fid][label_id];
  }

  fid_t fnum() { return fnum_; }

  size_t GetTotalNodesNum() const {
    size_t num = 0;
    for (auto& vec : oid_arrays_) {
      for (auto& v : vec) {
        num += v->length();
      }
    }
    return num;
  }

  size_t GetTotalNodesNum(label_id_t label) const {
    size_t num = 0;
    for (auto& vec : oid_arrays_) {
      num += vec[label]->length();
    }
    return num;
  }

  label_id_t label_num() const { return label_num_; }

  vid_t GetInnerVertexSize(fid_t fid) const {
    size_t num = 0;
    for (auto& v : oid_arrays_[fid]) {
      num += v->length();
    }
    return static_cast<vid_t>(num);
  }

  vid_t GetInnerVertexSize(fid_t fid, label_id_t label_id) const {
    return static_cast<vid_t>(oid_arrays_[fid][label_id]->length());
  }

  ObjectID AddVertices(
      Client& client,
      const std::map<label_id_t, std::vector<std::shared_ptr<oid_array_t>>>&
          oid_arrays_map) {
    int extra_label_num = oid_arrays_map.size();

    std::vector<std::vector<std::shared_ptr<oid_array_t>>> oid_arrays;
    oid_arrays.resize(extra_label_num);
    for (auto& pair : oid_arrays_map) {
      oid_arrays[pair.first - label_num_] = pair.second;
    }
    return AddNewVertexLabels(client, oid_arrays);
  }

  ObjectID AddNewVertexLabels(
      Client& client,
      const std::vector<std::vector<std::shared_ptr<oid_array_t>>>&
          oid_arrays) {
    size_t extra_label_num = oid_arrays.size();
    int task_num = static_cast<int>(fnum_) * static_cast<int>(extra_label_num);

    std::vector<std::vector<typename InternalType<oid_t>::vineyard_array_type>>
        vy_oid_arrays;
    std::vector<std::vector<vineyard::Hashmap<oid_t, vid_t>>> vy_o2g;
    int total_label_num = label_num_ + extra_label_num;
    vy_oid_arrays.resize(fnum_);
    vy_o2g.resize(fnum_);
    for (fid_t i = 0; i < fnum_; ++i) {
      vy_oid_arrays[i].resize(extra_label_num);
      vy_o2g[i].resize(extra_label_num);
    }

    int thread_num = std::min(
        static_cast<int>(std::thread::hardware_concurrency()), task_num);
    std::atomic<int> task_id(0);
    std::vector<std::thread> threads(thread_num);
    for (int i = 0; i < thread_num; ++i) {
      threads[i] = std::thread([&]() {
        while (true) {
          int got_task_id = task_id.fetch_add(1);
          if (got_task_id >= task_num) {
            break;
          }
          fid_t cur_fid = static_cast<fid_t>(got_task_id) % fnum_;
          auto cur_label =
              static_cast<label_id_t>(static_cast<fid_t>(got_task_id) / fnum_);

          vineyard::HashmapBuilder<oid_t, vid_t> builder(client);
          auto array = oid_arrays[cur_label][cur_fid];
          {
            vid_t cur_gid =
                id_parser_.GenerateId(cur_fid, label_num_ + cur_label, 0);
            int64_t vnum = array->length();
            // builder.reserve(static_cast<size_t>(vnum));
            for (int64_t k = 0; k < vnum; ++k) {
              builder.emplace(array->GetView(k), cur_gid);
              ++cur_gid;
            }
          }

          {
            typename InternalType<oid_t>::vineyard_builder_type array_builder(
                client, array);
            vy_oid_arrays[cur_fid][cur_label] =
                *std::dynamic_pointer_cast<vineyard::NumericArray<oid_t>>(
                    array_builder.Seal(client));

            vy_o2g[cur_fid][cur_label] =
                *std::dynamic_pointer_cast<vineyard::Hashmap<oid_t, vid_t>>(
                    builder.Seal(client));
          }
        }
      });
    }
    for (auto& thrd : threads) {
      thrd.join();
    }

    vineyard::ObjectMeta old_meta, new_meta;
    VINEYARD_CHECK_OK(client.GetMetaData(this->id(), old_meta));

    new_meta.SetTypeName(type_name<ArrowVertexMap<oid_t, vid_t>>());

    new_meta.AddKeyValue("fnum", fnum_);
    new_meta.AddKeyValue("label_num", total_label_num);

    size_t nbytes = 0;
    for (fid_t i = 0; i < fnum_; ++i) {
      for (label_id_t j = 0; j < total_label_num; ++j) {
        std::string array_name =
            "oid_arrays_" + std::to_string(i) + "_" + std::to_string(j);
        std::string map_name =
            "o2g_" + std::to_string(i) + "_" + std::to_string(j);
        if (j < label_num_) {
          auto array_meta = old_meta.GetMemberMeta(array_name);
          new_meta.AddMember(array_name, array_meta);
          nbytes += array_meta.GetNBytes();

          auto map_meta = old_meta.GetMemberMeta(map_name);
          new_meta.AddMember(map_name, map_meta);
          nbytes += map_meta.GetNBytes();
        } else {
          new_meta.AddMember(array_name,
                             vy_oid_arrays[i][j - label_num_].meta());
          nbytes += vy_oid_arrays[i][j - label_num_].nbytes();

          new_meta.AddMember(map_name, vy_o2g[i][j - label_num_].meta());
          nbytes += vy_o2g[i][j - label_num_].nbytes();
        }
      }
    }

    new_meta.SetNBytes(nbytes);
    ObjectID ret;
    VINEYARD_CHECK_OK(client.CreateMetaData(new_meta, ret));
    return ret;
  }

 private:
  fid_t fnum_;
  label_id_t label_num_;

  vineyard::IdParser<vid_t> id_parser_;

  // frag->label->oid
  std::vector<std::vector<std::shared_ptr<oid_array_t>>> oid_arrays_;
  std::vector<std::vector<vineyard::Hashmap<oid_t, vid_t>>> o2g_;

  friend class ArrowVertexMapBuilder<OID_T, VID_T>;

  friend class gs::ArrowProjectedVertexMap<OID_T, VID_T>;
};

template <typename VID_T>
class ArrowVertexMap<arrow::util::string_view, VID_T>
    : public vineyard::Registered<
          ArrowVertexMap<arrow::util::string_view, VID_T>> {
  using oid_t = arrow::util::string_view;
  using vid_t = VID_T;
  using label_id_t = property_graph_types::LABEL_ID_TYPE;
  using oid_array_t = arrow::LargeStringArray;

 public:
  ArrowVertexMap() {}
  ~ArrowVertexMap() {}

  static std::unique_ptr<vineyard::Object> Create() __attribute__((used)) {
    return std::static_pointer_cast<vineyard::Object>(
        std::unique_ptr<ArrowVertexMap<oid_t, vid_t>>{
            new ArrowVertexMap<oid_t, vid_t>()});
  }

  void Construct(const vineyard::ObjectMeta& meta) {
    this->meta_ = meta;
    this->id_ = meta.GetId();

    this->fnum_ = meta.GetKeyValue<fid_t>("fnum");
    this->label_num_ = meta.GetKeyValue<label_id_t>("label_num");

    id_parser_.Init(fnum_, label_num_);

    oid_arrays_.resize(fnum_);
    for (fid_t i = 0; i < fnum_; ++i) {
      oid_arrays_[i].resize(label_num_);
      for (label_id_t j = 0; j < label_num_; ++j) {
        typename InternalType<oid_t>::vineyard_array_type array;
        array.Construct(meta.GetMemberMeta("oid_arrays_" + std::to_string(i) +
                                           "_" + std::to_string(j)));
        oid_arrays_[i][j] = array.GetArray();
      }
    }

    initHashmaps();
  }

  bool GetOid(vid_t gid, oid_t& oid) const {
    fid_t fid = id_parser_.GetFid(gid);
    label_id_t label = id_parser_.GetLabelId(gid);
    int64_t offset = id_parser_.GetOffset(gid);
    if (fid < fnum_ && label < label_num_ && label >= 0) {
      auto array = oid_arrays_[fid][label];
      if (offset < array->length()) {
        oid = array->GetView(offset);
        return true;
      }
    }
    return false;
  }

  bool GetGid(fid_t fid, label_id_t label_id, oid_t oid, vid_t& gid) const {
    auto iter = o2g_[fid][label_id].find(oid);
    if (iter != o2g_[fid][label_id].end()) {
      gid = iter->second;
      return true;
    }
    return false;
  }

  bool GetGid(label_id_t label_id, oid_t oid, vid_t& gid) const {
    for (fid_t i = 0; i < fnum_; ++i) {
      if (GetGid(i, label_id, oid, gid)) {
        return true;
      }
    }
    return false;
  }

  std::vector<oid_t> GetOids(fid_t fid, label_id_t label_id) {
    auto array = oid_arrays_[fid][label_id];
    std::vector<oid_t> oids;

    oids.resize(array->length());
    for (auto i = 0; i < array->length(); i++) {
      oids[i] = array->GetView(i);
    }

    return oids;
  }

  fid_t fnum() { return fnum_; }

  size_t GetTotalNodesNum() const {
    size_t num = 0;
    for (auto& vec : oid_arrays_) {
      for (auto& v : vec) {
        num += v->length();
      }
    }
    return num;
  }

  size_t GetTotalNodesNum(label_id_t label) const {
    size_t num = 0;
    for (auto& vec : oid_arrays_) {
      num += vec[label]->length();
    }
    return num;
  }

  label_id_t label_num() const { return label_num_; }

  vid_t GetInnerVertexSize(fid_t fid) const {
    size_t num = 0;
    for (auto& v : oid_arrays_[fid]) {
      num += v->length();
    }
    return static_cast<vid_t>(num);
  }

  vid_t GetInnerVertexSize(fid_t fid, label_id_t label_id) const {
    return static_cast<vid_t>(oid_arrays_[fid][label_id]->length());
  }

  ObjectID AddVertices(
      Client& client,
      const std::map<label_id_t, std::vector<std::shared_ptr<oid_array_t>>>&
          oid_arrays_map) {
    int extra_label_num = oid_arrays_map.size();

    std::vector<std::vector<std::shared_ptr<oid_array_t>>> oid_arrays;
    oid_arrays.resize(extra_label_num);
    for (auto& pair : oid_arrays_map) {
      oid_arrays[pair.first - label_num_] = pair.second;
    }
    return AddNewVertexLabels(client, oid_arrays);
  }

  ObjectID AddNewVertexLabels(
      Client& client,
      const std::vector<std::vector<std::shared_ptr<oid_array_t>>>&
          oid_arrays) {
    size_t extra_label_num = oid_arrays.size();

    std::vector<std::vector<typename InternalType<oid_t>::vineyard_array_type>>
        vy_oid_arrays;
    int total_label_num = label_num_ + extra_label_num;
    vy_oid_arrays.resize(fnum_);
    for (fid_t i = 0; i < fnum_; ++i) {
      vy_oid_arrays[i].resize(extra_label_num);
    }

    ThreadGroup tg;
    auto builder_fn = [&client, &oid_arrays, &vy_oid_arrays](
                          fid_t const fid,
                          label_id_t const vlabel_id) -> Status {
      auto& array = oid_arrays[vlabel_id][fid];
      typename InternalType<oid_t>::vineyard_builder_type array_builder(client,
                                                                        array);
      vy_oid_arrays[fid][vlabel_id] = *std::dynamic_pointer_cast<
          typename InternalType<oid_t>::vineyard_array_type>(
          array_builder.Seal(client));
      return Status::OK();
    };

    for (fid_t fid = 0; fid < fnum_; ++fid) {
      for (size_t vlabel_id = 0; vlabel_id < extra_label_num; ++vlabel_id) {
        tg.AddTask(builder_fn, fid, vlabel_id);
      }
    }
    tg.TakeResults();

    vineyard::ObjectMeta old_meta, new_meta;
    VINEYARD_CHECK_OK(client.GetMetaData(this->id(), old_meta));

    new_meta.SetTypeName(type_name<ArrowVertexMap<oid_t, vid_t>>());

    new_meta.AddKeyValue("fnum", fnum_);
    new_meta.AddKeyValue("label_num", total_label_num);

    size_t nbytes = 0;
    for (fid_t i = 0; i < fnum_; ++i) {
      for (label_id_t j = 0; j < total_label_num; ++j) {
        std::string array_name =
            "oid_arrays_" + std::to_string(i) + "_" + std::to_string(j);
        if (j < label_num_) {
          auto array_meta = old_meta.GetMemberMeta(array_name);
          new_meta.AddMember(array_name, array_meta);
          nbytes += array_meta.GetNBytes();
        } else {
          new_meta.AddMember(array_name,
                             vy_oid_arrays[i][j - label_num_].meta());
          nbytes += vy_oid_arrays[i][j - label_num_].nbytes();
        }
      }
    }
    new_meta.SetNBytes(nbytes);
    ObjectID ret;
    VINEYARD_CHECK_OK(client.CreateMetaData(new_meta, ret));
    return ret;
  }

 private:
  void initHashmaps() {
    o2g_.resize(fnum_);
    for (fid_t i = 0; i < fnum_; ++i) {
      o2g_[i].resize(label_num_);
      for (label_id_t j = 0; j < label_num_; ++j) {
        auto array = oid_arrays_[i][j];
        auto& map = o2g_[i][j];
        {
          vid_t cur_gid = id_parser_.GenerateId(i, j, 0);
          int64_t vnum = array->length();
          for (int64_t k = 0; k < vnum; ++k) {
            map.emplace(array->GetView(k), cur_gid);
            ++cur_gid;
          }
        }
      }
    }
  }

  fid_t fnum_;
  label_id_t label_num_;

  vineyard::IdParser<vid_t> id_parser_;

  // frag->label->oid
  std::vector<std::vector<std::shared_ptr<oid_array_t>>> oid_arrays_;
  std::vector<std::vector<ska::flat_hash_map<oid_t, vid_t>>> o2g_;

  friend class ArrowVertexMapBuilder<arrow::util::string_view, VID_T>;

  friend class gs::ArrowProjectedVertexMap<arrow::util::string_view, VID_T>;
};

template <typename OID_T, typename VID_T>
class ArrowVertexMapBuilder : public vineyard::ObjectBuilder {
  using oid_t = OID_T;
  using vid_t = VID_T;
  using label_id_t = property_graph_types::LABEL_ID_TYPE;

 public:
  explicit ArrowVertexMapBuilder(vineyard::Client& client) {}

  void set_fnum_label_num(fid_t fnum, label_id_t label_num) {
    fnum_ = fnum;
    label_num_ = label_num;
    oid_arrays_.resize(fnum_);
    o2g_.resize(fnum_);
    for (fid_t i = 0; i < fnum_; ++i) {
      oid_arrays_[i].resize(label_num_);
      o2g_[i].resize(label_num_);
    }
  }

  void set_oid_array(
      fid_t fid, label_id_t label,
      const typename InternalType<oid_t>::vineyard_array_type& array) {
    oid_arrays_[fid][label] = array;
  }

  void set_o2g(fid_t fid, label_id_t label,
               const vineyard::Hashmap<oid_t, vid_t>& rm) {
    o2g_[fid][label] = rm;
  }

  std::shared_ptr<vineyard::Object> _Seal(vineyard::Client& client) {
    // ensure the builder hasn't been sealed yet.
    ENSURE_NOT_SEALED(this);

    VINEYARD_CHECK_OK(this->Build(client));

    auto vertex_map = std::make_shared<ArrowVertexMap<oid_t, vid_t>>();
    vertex_map->fnum_ = fnum_;
    vertex_map->label_num_ = label_num_;
    vertex_map->id_parser_.Init(fnum_, label_num_);

    vertex_map->oid_arrays_.resize(fnum_);
    for (fid_t i = 0; i < fnum_; ++i) {
      auto& array = vertex_map->oid_arrays_[i];
      array.resize(label_num_);
      for (label_id_t j = 0; j < label_num_; ++j) {
        array[j] = oid_arrays_[i][j].GetArray();
      }
    }

    vertex_map->o2g_ = o2g_;

    vertex_map->meta_.SetTypeName(type_name<ArrowVertexMap<oid_t, vid_t>>());

    vertex_map->meta_.AddKeyValue("fnum", fnum_);
    vertex_map->meta_.AddKeyValue("label_num", label_num_);

    size_t nbytes = 0;
    for (fid_t i = 0; i < fnum_; ++i) {
      for (label_id_t j = 0; j < label_num_; ++j) {
        vertex_map->meta_.AddMember(
            "oid_arrays_" + std::to_string(i) + "_" + std::to_string(j),
            oid_arrays_[i][j].meta());
        nbytes += oid_arrays_[i][j].nbytes();

        vertex_map->meta_.AddMember(
            "o2g_" + std::to_string(i) + "_" + std::to_string(j),
            o2g_[i][j].meta());
        nbytes += o2g_[i][j].nbytes();
      }
    }

    vertex_map->meta_.SetNBytes(nbytes);

    VINEYARD_CHECK_OK(
        client.CreateMetaData(vertex_map->meta_, vertex_map->id_));
    // mark the builder as sealed
    this->set_sealed(true);

    return std::static_pointer_cast<vineyard::Object>(vertex_map);
  }

 private:
  fid_t fnum_;
  label_id_t label_num_;

  std::vector<std::vector<typename InternalType<oid_t>::vineyard_array_type>>
      oid_arrays_;
  std::vector<std::vector<vineyard::Hashmap<oid_t, vid_t>>> o2g_;
};

template <typename VID_T>
class ArrowVertexMapBuilder<arrow::util::string_view, VID_T>
    : public vineyard::ObjectBuilder {
  using oid_t = arrow::util::string_view;
  using vid_t = VID_T;
  using label_id_t = property_graph_types::LABEL_ID_TYPE;

 public:
  explicit ArrowVertexMapBuilder(vineyard::Client& client) {}

  void set_fnum_label_num(fid_t fnum, label_id_t label_num) {
    fnum_ = fnum;
    label_num_ = label_num;
    oid_arrays_.resize(fnum_);
    for (fid_t i = 0; i < fnum_; ++i) {
      oid_arrays_[i].resize(label_num_);
    }
  }

  void set_oid_array(
      fid_t fid, label_id_t label,
      const typename InternalType<oid_t>::vineyard_array_type& array) {
    oid_arrays_[fid][label] = array;
  }

  std::shared_ptr<vineyard::Object> _Seal(vineyard::Client& client) {
    // ensure the builder hasn't been sealed yet.
    ENSURE_NOT_SEALED(this);

    VINEYARD_CHECK_OK(this->Build(client));

    auto vertex_map =
        std::make_shared<ArrowVertexMap<arrow::util::string_view, vid_t>>();
    vertex_map->fnum_ = fnum_;
    vertex_map->label_num_ = label_num_;
    vertex_map->id_parser_.Init(fnum_, label_num_);

    vertex_map->oid_arrays_.resize(fnum_);
    for (fid_t i = 0; i < fnum_; ++i) {
      auto& array = vertex_map->oid_arrays_[i];
      array.resize(label_num_);
      for (label_id_t j = 0; j < label_num_; ++j) {
        array[j] = oid_arrays_[i][j].GetArray();
      }
    }

    vertex_map->meta_.SetTypeName(type_name<ArrowVertexMap<oid_t, vid_t>>());

    vertex_map->meta_.AddKeyValue("fnum", fnum_);
    vertex_map->meta_.AddKeyValue("label_num", label_num_);

    size_t nbytes = 0;
    for (fid_t i = 0; i < fnum_; ++i) {
      for (label_id_t j = 0; j < label_num_; ++j) {
        vertex_map->meta_.AddMember(
            "oid_arrays_" + std::to_string(i) + "_" + std::to_string(j),
            oid_arrays_[i][j].meta());
        nbytes += oid_arrays_[i][j].nbytes();
      }
    }

    vertex_map->meta_.SetNBytes(nbytes);
    VINEYARD_CHECK_OK(
        client.CreateMetaData(vertex_map->meta_, vertex_map->id_));
    // mark the builder as sealed
    this->set_sealed(true);

    return std::static_pointer_cast<vineyard::Object>(vertex_map);
  }

 private:
  fid_t fnum_;
  label_id_t label_num_;

  std::vector<std::vector<typename InternalType<oid_t>::vineyard_array_type>>
      oid_arrays_;
};

template <typename OID_T, typename VID_T>
class BasicArrowVertexMapBuilder : public ArrowVertexMapBuilder<OID_T, VID_T> {
  using oid_t = OID_T;
  using vid_t = VID_T;
  using oid_array_t = typename vineyard::ConvertToArrowType<oid_t>::ArrayType;
  using label_id_t = property_graph_types::LABEL_ID_TYPE;

 public:
  BasicArrowVertexMapBuilder(
      vineyard::Client& client, fid_t fnum, label_id_t label_num,
      const std::vector<std::vector<std::shared_ptr<oid_array_t>>>& oid_arrays)
      : ArrowVertexMapBuilder<oid_t, vid_t>(client),
        fnum_(fnum),
        label_num_(label_num),
        oid_arrays_(oid_arrays) {
    CHECK_EQ(oid_arrays.size(), label_num);
    id_parser_.Init(fnum_, label_num_);
  }

  vineyard::Status Build(vineyard::Client& client) override {
    this->set_fnum_label_num(fnum_, label_num_);

#if 0
    for (fid_t i = 0; i < fnum_; ++i) {
      // TODO(luoxiaojian): parallel construct hashmap
      for (label_id_t j = 0; j < label_num_; ++j) {
        vineyard::HashmapBuilder<oid_t, vid_t> builder(client);

        auto array = oid_arrays_[j][i];
        {
          vid_t cur_gid = id_parser_.GenerateId(i, j, 0);
          int64_t vnum = array->length();
          for (int64_t k = 0; k < vnum; ++k) {
            builder.emplace(array->GetView(k), cur_gid);
            ++cur_gid;
          }
        }

        typename InternalType<oid_t>::vineyard_builder_type array_builder(
            client, array);
        this->set_oid_array(
            i, j,
            *std::dynamic_pointer_cast<vineyard::NumericArray<oid_t>>(
                array_builder.Seal(client)));

        this->set_o2g(
            i, j,
            *std::dynamic_pointer_cast<vineyard::Hashmap<oid_t, vid_t>>(
                builder.Seal(client)));
      }
    }
#else
    int task_num = static_cast<int>(fnum_) * static_cast<int>(label_num_);
    int thread_num = std::min(
        static_cast<int>(std::thread::hardware_concurrency()), task_num);
    std::atomic<int> task_id(0);

#if defined(WITH_PROFILING)
    auto start_ts = GetCurrentTime();
#endif

    std::vector<std::thread> threads(thread_num);
    for (int i = 0; i < thread_num; ++i) {
      threads[i] = std::thread([&]() {
        while (true) {
          int got_task_id = task_id.fetch_add(1);
          if (got_task_id >= task_num) {
            break;
          }
          fid_t cur_fid = static_cast<fid_t>(got_task_id) % fnum_;
          label_id_t cur_label =
              static_cast<label_id_t>(static_cast<fid_t>(got_task_id) / fnum_);

          vineyard::HashmapBuilder<oid_t, vid_t> builder(client);
          auto array = oid_arrays_[cur_label][cur_fid];
          {
            vid_t cur_gid = id_parser_.GenerateId(cur_fid, cur_label, 0);
            int64_t vnum = array->length();
            // builder.reserve(static_cast<size_t>(vnum));
            for (int64_t k = 0; k < vnum; ++k) {
              builder.emplace(array->GetView(k), cur_gid);
              ++cur_gid;
            }
          }

          {
            typename InternalType<oid_t>::vineyard_builder_type array_builder(
                client, array);
            this->set_oid_array(
                cur_fid, cur_label,
                *std::dynamic_pointer_cast<vineyard::NumericArray<oid_t>>(
                    array_builder.Seal(client)));

            this->set_o2g(
                cur_fid, cur_label,
                *std::dynamic_pointer_cast<vineyard::Hashmap<oid_t, vid_t>>(
                    builder.Seal(client)));
          }
        }
      });
    }
    for (auto& thrd : threads) {
      thrd.join();
    }

#if defined(WITH_PROFILING)
    auto finish_seal_ts = GetCurrentTime();
    LOG(INFO) << "Seal hashmaps uses " << (finish_seal_ts - start_ts)
              << " seconds";
#endif

#endif

    return vineyard::Status::OK();
  }

 private:
  fid_t fnum_;
  label_id_t label_num_;

  vineyard::IdParser<vid_t> id_parser_;

  std::vector<std::vector<std::shared_ptr<oid_array_t>>> oid_arrays_;
};

template <typename VID_T>
class BasicArrowVertexMapBuilder<arrow::util::string_view, VID_T>
    : public ArrowVertexMapBuilder<arrow::util::string_view, VID_T> {
  using oid_t = arrow::util::string_view;
  using vid_t = VID_T;
  using oid_array_t = arrow::LargeStringArray;
  using label_id_t = property_graph_types::LABEL_ID_TYPE;

 public:
  BasicArrowVertexMapBuilder(
      vineyard::Client& client, fid_t fnum, label_id_t label_num,
      const std::vector<std::vector<std::shared_ptr<oid_array_t>>>& oid_arrays)
      : ArrowVertexMapBuilder<arrow::util::string_view, vid_t>(client),
        fnum_(fnum),
        label_num_(label_num),
        oid_arrays_(oid_arrays) {
    CHECK_EQ(oid_arrays.size(), label_num);
    id_parser_.Init(fnum_, label_num_);
  }

  vineyard::Status Build(vineyard::Client& client) override {
    this->set_fnum_label_num(fnum_, label_num_);

    ThreadGroup tg;

    auto builder_fn = [this, &client](fid_t const fid,
                                      label_id_t const vlabel_id) -> Status {
      auto& array = oid_arrays_[vlabel_id][fid];
      typename InternalType<oid_t>::vineyard_builder_type array_builder(client,
                                                                        array);
      this->set_oid_array(
          fid, vlabel_id,
          *std::dynamic_pointer_cast<
              typename InternalType<oid_t>::vineyard_array_type>(
              array_builder.Seal(client)));
      return Status::OK();
    };

    for (fid_t fid = 0; fid < fnum_; ++fid) {
      for (label_id_t vlabel_id = 0; vlabel_id < label_num_; ++vlabel_id) {
        tg.AddTask(builder_fn, fid, vlabel_id);
      }
    }
    tg.TakeResults();
    return vineyard::Status::OK();
  }

 private:
  fid_t fnum_;
  label_id_t label_num_;

  vineyard::IdParser<vid_t> id_parser_;

  std::vector<std::vector<std::shared_ptr<oid_array_t>>> oid_arrays_;
};

}  // namespace vineyard

#endif  // MODULES_GRAPH_VERTEX_MAP_ARROW_VERTEX_MAP_H_
