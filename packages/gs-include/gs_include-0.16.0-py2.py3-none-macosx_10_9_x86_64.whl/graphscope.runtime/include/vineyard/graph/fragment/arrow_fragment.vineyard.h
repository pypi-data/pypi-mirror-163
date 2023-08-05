#ifndef MODULES_GRAPH_FRAGMENT_ARROW_FRAGMENT_VINEYARD_H
#define MODULES_GRAPH_FRAGMENT_ARROW_FRAGMENT_VINEYARD_H

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

#ifndef MODULES_GRAPH_FRAGMENT_ARROW_FRAGMENT_MOD_H_
#define MODULES_GRAPH_FRAGMENT_ARROW_FRAGMENT_MOD_H_

#include <algorithm>
#include <cstddef>
#include <map>
#include <memory>
#include <set>
#include <string>
#include <thread>
#include <unordered_map>
#include <utility>
#include <vector>

#include "arrow/api.h"
#include "arrow/io/api.h"
#include "boost/algorithm/string.hpp"

#include "grape/fragment/fragment_base.h"
#include "grape/graph/adj_list.h"
#include "grape/utils/vertex_array.h"

#include "client/ds/core_types.h"
#include "client/ds/object_meta.h"

#include "basic/ds/arrow.h"
#include "basic/ds/arrow_utils.h"
#include "common/util/functions.h"
#include "common/util/typename.h"

#include "graph/fragment/fragment_traits.h"
#include "graph/fragment/graph_schema.h"
#include "graph/fragment/property_graph_types.h"
#include "graph/fragment/property_graph_utils.h"
#include "graph/utils/context_protocols.h"
#include "graph/utils/error.h"
#include "graph/utils/thread_group.h"
#include "graph/vertex_map/arrow_vertex_map.h"

namespace gs {

template <typename OID_T, typename VID_T, typename VDATA_T, typename EDATA_T>
class ArrowProjectedFragment;

}  // namespace gs

namespace vineyard {

inline std::string generate_name_with_suffix(
    const std::string& prefix, property_graph_types::LABEL_ID_TYPE label) {
  return prefix + "_" + std::to_string(label);
}

inline std::string generate_name_with_suffix(
    const std::string& prefix, property_graph_types::LABEL_ID_TYPE v_label,
    property_graph_types::LABEL_ID_TYPE e_label) {
  return prefix + "_" + std::to_string(v_label) + "_" + std::to_string(e_label);
}

class ArrowFragmentBase : public vineyard::Object {
 public:
  using prop_id_t = property_graph_types::PROP_ID_TYPE;
  using label_id_t = property_graph_types::LABEL_ID_TYPE;

  virtual ~ArrowFragmentBase() = default;

  virtual boost::leaf::result<vineyard::ObjectID> AddVertexColumns(
      vineyard::Client& client,
      const std::map<
          label_id_t,
          std::vector<std::pair<std::string, std::shared_ptr<arrow::Array>>>>
          columns,
      bool replace = false) = 0;

  virtual boost::leaf::result<vineyard::ObjectID> AddVertexColumns(
      vineyard::Client& client,
      const std::map<label_id_t,
                     std::vector<std::pair<
                         std::string, std::shared_ptr<arrow::ChunkedArray>>>>
          columns,
      bool replace = false) {
    VINEYARD_ASSERT(false, "Not implemented");
    return vineyard::InvalidObjectID();
  }

  virtual vineyard::ObjectID vertex_map_id() const = 0;

  virtual const PropertyGraphSchema& schema() const = 0;

  virtual bool directed() const = 0;

  virtual bool is_multigraph() const = 0;

  virtual const std::string vid_typename() const = 0;

  virtual const std::string oid_typename() const = 0;
};

template <typename OID_T, typename VID_T>
class ArrowFragmentBaseBuilder;

template <typename OID_T, typename VID_T>
class __attribute__((annotate("vineyard"))) ArrowFragment
    : public ArrowFragmentBase,
      public vineyard::BareRegistered<ArrowFragment<OID_T, VID_T>> {
 
  public:
    static std::unique_ptr<Object> Create() __attribute__((used)) {
        return std::static_pointer_cast<Object>(
            std::unique_ptr<ArrowFragment<OID_T, VID_T>>{
                new ArrowFragment<OID_T, VID_T>()});
    }


  public:
    void Construct(const ObjectMeta& meta) override {
        std::string __type_name = type_name<ArrowFragment<OID_T, VID_T>>();
        VINEYARD_ASSERT(
            meta.GetTypeName() == __type_name,
            "Expect typename '" + __type_name + "', but got '" + meta.GetTypeName() + "'");
        this->meta_ = meta;
        this->id_ = meta.GetId();

        meta.GetKeyValue("fid_", this->fid_);
        meta.GetKeyValue("fnum_", this->fnum_);
        meta.GetKeyValue("directed_", this->directed_);
        meta.GetKeyValue("is_multigraph_", this->is_multigraph_);
        meta.GetKeyValue("vertex_label_num_", this->vertex_label_num_);
        meta.GetKeyValue("edge_label_num_", this->edge_label_num_);
        meta.GetKeyValue("oid_type", this->oid_type);
        meta.GetKeyValue("vid_type", this->vid_type);
        this->ivnums_.Construct(meta.GetMemberMeta("ivnums_"));
        this->ovnums_.Construct(meta.GetMemberMeta("ovnums_"));
        this->tvnums_.Construct(meta.GetMemberMeta("tvnums_"));
        for (size_t __idx = 0; __idx < meta.GetKeyValue<size_t>("__vertex_tables_-size"); ++__idx) {
            this->vertex_tables_.emplace_back(std::dynamic_pointer_cast<Table>(
                    meta.GetMember("__vertex_tables_-" + std::to_string(__idx))));
        }
        for (size_t __idx = 0; __idx < meta.GetKeyValue<size_t>("__ovgid_lists_-size"); ++__idx) {
            this->ovgid_lists_.emplace_back(std::dynamic_pointer_cast<ArrowFragment::vid_vineyard_array_t>(
                    meta.GetMember("__ovgid_lists_-" + std::to_string(__idx))));
        }
        for (size_t __idx = 0; __idx < meta.GetKeyValue<size_t>("__ovg2l_maps_-size"); ++__idx) {
            this->ovg2l_maps_.emplace_back(std::dynamic_pointer_cast<Hashmap<vid_t, vid_t>>(
                    meta.GetMember("__ovg2l_maps_-" + std::to_string(__idx))));
        }
        for (size_t __idx = 0; __idx < meta.GetKeyValue<size_t>("__edge_tables_-size"); ++__idx) {
            this->edge_tables_.emplace_back(std::dynamic_pointer_cast<Table>(
                    meta.GetMember("__edge_tables_-" + std::to_string(__idx))));
        }
        this->ie_lists_.resize(meta.GetKeyValue<size_t>("__ie_lists_-size"));
        for (size_t __idx = 0; __idx < this->ie_lists_.size(); ++__idx) {
            for (size_t __idy = 0; __idy < meta.GetKeyValue<size_t>(
                    "__ie_lists_-" + std::to_string(__idx) + "-size"); ++__idy) {
                this->ie_lists_[__idx].emplace_back(std::dynamic_pointer_cast<FixedSizeBinaryArray>(
                    meta.GetMember("__ie_lists_-" + std::to_string(__idx) + "-" + std::to_string(__idy))));
            }
        }
        this->oe_lists_.resize(meta.GetKeyValue<size_t>("__oe_lists_-size"));
        for (size_t __idx = 0; __idx < this->oe_lists_.size(); ++__idx) {
            for (size_t __idy = 0; __idy < meta.GetKeyValue<size_t>(
                    "__oe_lists_-" + std::to_string(__idx) + "-size"); ++__idy) {
                this->oe_lists_[__idx].emplace_back(std::dynamic_pointer_cast<FixedSizeBinaryArray>(
                    meta.GetMember("__oe_lists_-" + std::to_string(__idx) + "-" + std::to_string(__idy))));
            }
        }
        this->ie_offsets_lists_.resize(meta.GetKeyValue<size_t>("__ie_offsets_lists_-size"));
        for (size_t __idx = 0; __idx < this->ie_offsets_lists_.size(); ++__idx) {
            for (size_t __idy = 0; __idy < meta.GetKeyValue<size_t>(
                    "__ie_offsets_lists_-" + std::to_string(__idx) + "-size"); ++__idy) {
                this->ie_offsets_lists_[__idx].emplace_back(std::dynamic_pointer_cast<Int64Array>(
                    meta.GetMember("__ie_offsets_lists_-" + std::to_string(__idx) + "-" + std::to_string(__idy))));
            }
        }
        this->oe_offsets_lists_.resize(meta.GetKeyValue<size_t>("__oe_offsets_lists_-size"));
        for (size_t __idx = 0; __idx < this->oe_offsets_lists_.size(); ++__idx) {
            for (size_t __idy = 0; __idy < meta.GetKeyValue<size_t>(
                    "__oe_offsets_lists_-" + std::to_string(__idx) + "-size"); ++__idy) {
                this->oe_offsets_lists_[__idx].emplace_back(std::dynamic_pointer_cast<Int64Array>(
                    meta.GetMember("__oe_offsets_lists_-" + std::to_string(__idx) + "-" + std::to_string(__idy))));
            }
        }
        this->vm_ptr_ = std::dynamic_pointer_cast<ArrowFragment::vertex_map_t>(meta.GetMember("vm_ptr_"));
        meta.GetKeyValue("schema_json_", this->schema_json_);

        
        if (meta.IsLocal()) {
            this->PostConstruct(meta);
        }
    }

 private:
public:
  using oid_t = OID_T;
  using vid_t = VID_T;
  using internal_oid_t = typename InternalType<oid_t>::type;
  using eid_t = property_graph_types::EID_TYPE;
  using prop_id_t = property_graph_types::PROP_ID_TYPE;
  using label_id_t = property_graph_types::LABEL_ID_TYPE;
  using vertex_range_t = grape::VertexRange<vid_t>;
  using inner_vertices_t = vertex_range_t;
  using outer_vertices_t = vertex_range_t;
  using vertices_t = vertex_range_t;
  using nbr_t = property_graph_utils::Nbr<vid_t, eid_t>;
  using nbr_unit_t = property_graph_utils::NbrUnit<vid_t, eid_t>;
  using adj_list_t = property_graph_utils::AdjList<vid_t, eid_t>;
  using raw_adj_list_t = property_graph_utils::RawAdjList<vid_t, eid_t>;
  using vertex_map_t = ArrowVertexMap<internal_oid_t, vid_t>;
  using vertex_t = grape::Vertex<vid_t>;

  using ovg2l_map_t =
      ska::flat_hash_map<vid_t, vid_t, typename Hashmap<vid_t, vid_t>::KeyHash>;

  using vid_array_t = typename vineyard::ConvertToArrowType<vid_t>::ArrayType;
  using vid_vineyard_array_t =
      typename vineyard::ConvertToArrowType<vid_t>::VineyardArrayType;
  using eid_array_t = typename vineyard::ConvertToArrowType<eid_t>::ArrayType;
  using eid_vineyard_array_t =
      typename vineyard::ConvertToArrowType<vid_t>::VineyardArrayType;

  using vid_builder_t = typename ConvertToArrowType<vid_t>::BuilderType;

  template <typename DATA_T>
  using vertex_array_t = grape::VertexArray<vertices_t, DATA_T>;

  template <typename DATA_T>
  using inner_vertex_array_t = grape::VertexArray<inner_vertices_t, DATA_T>;

  template <typename DATA_T>
  using outer_vertex_array_t = grape::VertexArray<outer_vertices_t, DATA_T>;

  static constexpr grape::LoadStrategy load_strategy =
      grape::LoadStrategy::kBothOutIn;

 public:
  ~ArrowFragment() = default;

  vineyard::ObjectID vertex_map_id() const override { return vm_ptr_->id(); }

  bool directed() const override { return directed_; }

  bool is_multigraph() const override { return is_multigraph_; }

  const std::string vid_typename() const override { return vid_type; }

  const std::string oid_typename() const override { return oid_type; }

  void PostConstruct(const vineyard::ObjectMeta& meta) override {
    vid_parser_.Init(fnum_, vertex_label_num_);
    this->schema_.FromJSON(schema_json_);

    // init pointers for arrays and tables
    initPointers();

    // init edge numbers
    oenum_ = 0;
    ienum_ = 0;
    for (label_id_t i = 0; i < vertex_label_num_; i++) {
      for (auto& v : InnerVertices(i)) {
        for (label_id_t j = 0; j < edge_label_num_; j++) {
          oenum_ += GetLocalOutDegree(v, j);
          ienum_ += GetLocalInDegree(v, j);
        }
      }
    }
  }

  fid_t fid() const { return fid_; }

  fid_t fnum() const { return fnum_; }

  label_id_t vertex_label(const vertex_t& v) const {
    return vid_parser_.GetLabelId(v.GetValue());
  }

  int64_t vertex_offset(const vertex_t& v) const {
    return vid_parser_.GetOffset(v.GetValue());
  }

  label_id_t vertex_label_num() const { return schema_.vertex_label_num(); }

  label_id_t edge_label_num() const { return schema_.edge_label_num(); }

  prop_id_t vertex_property_num(label_id_t label) const {
    std::string type = "VERTEX";
    return static_cast<prop_id_t>(schema_.GetEntry(label, type).property_num());
  }

  std::shared_ptr<arrow::DataType> vertex_property_type(label_id_t label,
                                                        prop_id_t prop) const {
    return vertex_tables_[label]->schema()->field(prop)->type();
  }

  prop_id_t edge_property_num(label_id_t label) const {
    std::string type = "EDGE";
    return static_cast<prop_id_t>(schema_.GetEntry(label, type).property_num());
  }

  std::shared_ptr<arrow::DataType> edge_property_type(label_id_t label,
                                                      prop_id_t prop) const {
    return edge_tables_[label]->schema()->field(prop)->type();
  }

  std::shared_ptr<arrow::Table> vertex_data_table(label_id_t i) const {
    return vertex_tables_[i]->GetTable();
  }

  std::shared_ptr<arrow::Table> edge_data_table(label_id_t i) const {
    return edge_tables_[i]->GetTable();
  }

  template <typename DATA_T>
  property_graph_utils::EdgeDataColumn<DATA_T, nbr_unit_t> edge_data_column(
      label_id_t label, prop_id_t prop) const {
    if (edge_tables_[label]->num_rows() == 0) {
      return property_graph_utils::EdgeDataColumn<DATA_T, nbr_unit_t>();
    } else {
      return property_graph_utils::EdgeDataColumn<DATA_T, nbr_unit_t>(
          edge_tables_[label]->column(prop)->chunk(0));
    }
  }

  template <typename DATA_T>
  property_graph_utils::VertexDataColumn<DATA_T, vid_t> vertex_data_column(
      label_id_t label, prop_id_t prop) const {
    if (vertex_tables_[label]->num_rows() == 0) {
      return property_graph_utils::VertexDataColumn<DATA_T, vid_t>(
          InnerVertices(label));
    } else {
      return property_graph_utils::VertexDataColumn<DATA_T, vid_t>(
          InnerVertices(label), vertex_tables_[label]->column(prop)->chunk(0));
    }
  }

  vertex_range_t Vertices(label_id_t label_id) const {
    return vertex_range_t(
        vid_parser_.GenerateId(0, label_id, 0),
        vid_parser_.GenerateId(0, label_id, tvnums_[label_id]));
  }

  vertex_range_t InnerVertices(label_id_t label_id) const {
    return vertex_range_t(
        vid_parser_.GenerateId(0, label_id, 0),
        vid_parser_.GenerateId(0, label_id, ivnums_[label_id]));
  }

  vertex_range_t OuterVertices(label_id_t label_id) const {
    return vertex_range_t(
        vid_parser_.GenerateId(0, label_id, ivnums_[label_id]),
        vid_parser_.GenerateId(0, label_id, tvnums_[label_id]));
  }

  vertex_range_t InnerVerticesSlice(label_id_t label_id, vid_t start, vid_t end)
      const {
    CHECK(start <= end && start <= ivnums_[label_id]);
    if (end <= ivnums_[label_id]) {
      return vertex_range_t(vid_parser_.GenerateId(0, label_id, start),
                            vid_parser_.GenerateId(0, label_id, end));
    } else {
      return vertex_range_t(
          vid_parser_.GenerateId(0, label_id, start),
          vid_parser_.GenerateId(0, label_id, ivnums_[label_id]));
    }
  }

  inline vid_t GetVerticesNum(label_id_t label_id) const {
    return tvnums_[label_id];
  }

  bool GetVertex(label_id_t label, const oid_t& oid, vertex_t& v) const {
    vid_t gid;
    if (vm_ptr_->GetGid(label, internal_oid_t(oid), gid)) {
      return (vid_parser_.GetFid(gid) == fid_) ? InnerVertexGid2Vertex(gid, v)
                                               : OuterVertexGid2Vertex(gid, v);
    } else {
      return false;
    }
  }

  oid_t GetId(const vertex_t& v) const {
    return IsInnerVertex(v) ? GetInnerVertexId(v) : GetOuterVertexId(v);
  }

  fid_t GetFragId(const vertex_t& u) const {
    return IsInnerVertex(u) ? fid_ : vid_parser_.GetFid(GetOuterVertexGid(u));
  }

  size_t GetTotalNodesNum() const { return vm_ptr_->GetTotalNodesNum(); }
  size_t GetTotalVerticesNum() const { return vm_ptr_->GetTotalNodesNum(); }
  size_t GetTotalVerticesNum(label_id_t label) const {
    return vm_ptr_->GetTotalNodesNum(label);
  }

  size_t GetEdgeNum() const { return directed_ ? oenum_ + ienum_ : oenum_; }

  size_t GetInEdgeNum() const { return ienum_; }

  size_t GetOutEdgeNum() const { return oenum_; }

  template <typename T>
  T GetData(const vertex_t& v, prop_id_t prop_id) const {
    return property_graph_utils::ValueGetter<T>::Value(
        vertex_tables_columns_[vid_parser_.GetLabelId(v.GetValue())][prop_id],
        vid_parser_.GetOffset(v.GetValue()));
  }

  bool HasChild(const vertex_t& v, label_id_t e_label) const {
    return GetLocalOutDegree(v, e_label) != 0;
  }

  bool HasParent(const vertex_t& v, label_id_t e_label) const {
    return GetLocalInDegree(v, e_label) != 0;
  }

  int GetLocalOutDegree(const vertex_t& v, label_id_t e_label) const {
    return GetOutgoingAdjList(v, e_label).Size();
  }

  int GetLocalInDegree(const vertex_t& v, label_id_t e_label) const {
    return GetIncomingAdjList(v, e_label).Size();
  }

  // FIXME: grape message buffer compatibility
  bool Gid2Vertex(const vid_t& gid, vertex_t& v) const {
    return (vid_parser_.GetFid(gid) == fid_) ? InnerVertexGid2Vertex(gid, v)
                                             : OuterVertexGid2Vertex(gid, v);
  }

  vid_t Vertex2Gid(const vertex_t& v) const {
    return IsInnerVertex(v) ? GetInnerVertexGid(v) : GetOuterVertexGid(v);
  }

  inline vid_t GetInnerVerticesNum(label_id_t label_id) const {
    return ivnums_[label_id];
  }

  inline vid_t GetOuterVerticesNum(label_id_t label_id) const {
    return ovnums_[label_id];
  }

  inline bool IsInnerVertex(const vertex_t& v) const {
    return vid_parser_.GetOffset(v.GetValue()) <
           static_cast<int64_t>(ivnums_[vid_parser_.GetLabelId(v.GetValue())]);
  }

  inline bool IsOuterVertex(const vertex_t& v) const {
    vid_t offset = vid_parser_.GetOffset(v.GetValue());
    label_id_t label = vid_parser_.GetLabelId(v.GetValue());
    return offset < tvnums_[label] && offset >= ivnums_[label];
  }

  bool GetInnerVertex(label_id_t label, const oid_t& oid, vertex_t& v) const {
    vid_t gid;
    if (vm_ptr_->GetGid(label, internal_oid_t(oid), gid)) {
      if (vid_parser_.GetFid(gid) == fid_) {
        v.SetValue(vid_parser_.GetLid(gid));
        return true;
      }
    }
    return false;
  }

  bool GetOuterVertex(label_id_t label, const oid_t& oid, vertex_t& v) const {
    vid_t gid;
    if (vm_ptr_->GetGid(label, internal_oid_t(oid), gid)) {
      return OuterVertexGid2Vertex(gid, v);
    }
    return false;
  }

  inline oid_t GetInnerVertexId(const vertex_t& v) const {
    internal_oid_t internal_oid;
    vid_t gid =
        vid_parser_.GenerateId(fid_, vid_parser_.GetLabelId(v.GetValue()),
                               vid_parser_.GetOffset(v.GetValue()));
    CHECK(vm_ptr_->GetOid(gid, internal_oid));
    return oid_t(internal_oid);
  }

  inline oid_t GetOuterVertexId(const vertex_t& v) const {
    vid_t gid = GetOuterVertexGid(v);
    internal_oid_t internal_oid;
    CHECK(vm_ptr_->GetOid(gid, internal_oid));
    return oid_t(internal_oid);
  }

  inline oid_t Gid2Oid(const vid_t& gid) const {
    internal_oid_t internal_oid;
    CHECK(vm_ptr_->GetOid(gid, internal_oid));
    return oid_t(internal_oid);
  }

  inline bool Oid2Gid(label_id_t label, const oid_t& oid, vid_t& gid) const {
    return vm_ptr_->GetGid(label, internal_oid_t(oid), gid);
  }

  inline bool Oid2Gid(label_id_t label, const oid_t& oid, vertex_t& v) const {
    vid_t gid;
    if (vm_ptr_->GetGid(label, internal_oid_t(oid), gid)) {
      v.SetValue(gid);
      return true;
    }
    return false;
  }

  inline bool InnerVertexGid2Vertex(const vid_t& gid, vertex_t& v) const {
    v.SetValue(vid_parser_.GetLid(gid));
    return true;
  }

  inline bool OuterVertexGid2Vertex(const vid_t& gid, vertex_t& v) const {
    auto map = ovg2l_maps_ptr_[vid_parser_.GetLabelId(gid)];
    auto iter = map->find(gid);
    if (iter != map->end()) {
      v.SetValue(iter->second);
      return true;
    } else {
      return false;
    }
  }

  inline vid_t GetOuterVertexGid(const vertex_t& v) const {
    label_id_t v_label = vid_parser_.GetLabelId(v.GetValue());
    return ovgid_lists_ptr_[v_label][vid_parser_.GetOffset(v.GetValue()) -
                                     static_cast<int64_t>(ivnums_[v_label])];
  }
  inline vid_t GetInnerVertexGid(const vertex_t& v) const {
    return vid_parser_.GenerateId(fid_, vid_parser_.GetLabelId(v.GetValue()),
                                  vid_parser_.GetOffset(v.GetValue()));
  }

  inline adj_list_t GetIncomingAdjList(const vertex_t& v, label_id_t e_label)
      const {
    vid_t vid = v.GetValue();
    label_id_t v_label = vid_parser_.GetLabelId(vid);
    int64_t v_offset = vid_parser_.GetOffset(vid);
    const int64_t* offset_array = ie_offsets_ptr_lists_[v_label][e_label];
    const nbr_unit_t* ie = ie_ptr_lists_[v_label][e_label];
    return adj_list_t(&ie[offset_array[v_offset]],
                      &ie[offset_array[v_offset + 1]],
                      flatten_edge_tables_columns_[e_label]);
  }

  inline raw_adj_list_t GetIncomingRawAdjList(const vertex_t& v,
                                              label_id_t e_label) const {
    vid_t vid = v.GetValue();
    label_id_t v_label = vid_parser_.GetLabelId(vid);
    int64_t v_offset = vid_parser_.GetOffset(vid);
    const int64_t* offset_array = ie_offsets_ptr_lists_[v_label][e_label];
    const nbr_unit_t* ie = ie_ptr_lists_[v_label][e_label];
    return raw_adj_list_t(&ie[offset_array[v_offset]],
                          &ie[offset_array[v_offset + 1]]);
  }

  inline adj_list_t GetOutgoingAdjList(const vertex_t& v, label_id_t e_label)
      const {
    vid_t vid = v.GetValue();
    label_id_t v_label = vid_parser_.GetLabelId(vid);
    int64_t v_offset = vid_parser_.GetOffset(vid);
    const int64_t* offset_array = oe_offsets_ptr_lists_[v_label][e_label];
    const nbr_unit_t* oe = oe_ptr_lists_[v_label][e_label];
    return adj_list_t(&oe[offset_array[v_offset]],
                      &oe[offset_array[v_offset + 1]],
                      flatten_edge_tables_columns_[e_label]);
  }

  inline raw_adj_list_t GetOutgoingRawAdjList(const vertex_t& v,
                                              label_id_t e_label) const {
    vid_t vid = v.GetValue();
    label_id_t v_label = vid_parser_.GetLabelId(vid);
    int64_t v_offset = vid_parser_.GetOffset(vid);
    const int64_t* offset_array = oe_offsets_ptr_lists_[v_label][e_label];
    const nbr_unit_t* oe = oe_ptr_lists_[v_label][e_label];
    return raw_adj_list_t(&oe[offset_array[v_offset]],
                          &oe[offset_array[v_offset + 1]]);
  }

  /**
   * N.B.: as an temporary solution, for POC of graph-learn, will be removed
   * later.
   */
  inline std::pair<int64_t, int64_t> GetOutgoingAdjOffsets(
      const vertex_t& v, label_id_t e_label) const {
    vid_t vid = v.GetValue();
    label_id_t v_label = vid_parser_.GetLabelId(vid);
    int64_t v_offset = vid_parser_.GetOffset(vid);
    const int64_t* offset_array = oe_offsets_ptr_lists_[v_label][e_label];
    const nbr_unit_t* oe = oe_ptr_lists_[v_label][e_label];
    return std::make_pair(offset_array[v_offset], offset_array[v_offset + 1]);
  }

  inline grape::DestList IEDests(const vertex_t& v, label_id_t e_label) const {
    int64_t offset = vid_parser_.GetOffset(v.GetValue());
    auto v_label = vertex_label(v);

    return grape::DestList(idoffset_[v_label][e_label][offset],
                           idoffset_[v_label][e_label][offset + 1]);
  }

  inline grape::DestList OEDests(const vertex_t& v, label_id_t e_label) const {
    int64_t offset = vid_parser_.GetOffset(v.GetValue());
    auto v_label = vertex_label(v);

    return grape::DestList(odoffset_[v_label][e_label][offset],
                           odoffset_[v_label][e_label][offset + 1]);
  }

  inline grape::DestList IOEDests(const vertex_t& v, label_id_t e_label) const {
    int64_t offset = vid_parser_.GetOffset(v.GetValue());
    auto v_label = vertex_label(v);

    return grape::DestList(iodoffset_[v_label][e_label][offset],
                           iodoffset_[v_label][e_label][offset + 1]);
  }

  std::shared_ptr<vertex_map_t> GetVertexMap() { return vm_ptr_; }

  const PropertyGraphSchema& schema() const override { return schema_; }

  void PrepareToRunApp(const grape::CommSpec& comm_spec,
                       grape::PrepareConf conf) {
    if (conf.message_strategy ==
        grape::MessageStrategy::kAlongEdgeToOuterVertex) {
      initDestFidList(true, true, iodst_, iodoffset_);
    } else if (conf.message_strategy ==
               grape::MessageStrategy::kAlongIncomingEdgeToOuterVertex) {
      initDestFidList(true, false, idst_, idoffset_);
    } else if (conf.message_strategy ==
               grape::MessageStrategy::kAlongOutgoingEdgeToOuterVertex) {
      initDestFidList(false, true, odst_, odoffset_);
    }
  }

  boost::leaf::result<ObjectID> AddVerticesAndEdges(
      Client & client,
      std::map<label_id_t, std::shared_ptr<arrow::Table>> && vertex_tables_map,
      std::map<label_id_t, std::shared_ptr<arrow::Table>> && edge_tables_map,
      ObjectID vm_id,
      const std::vector<std::set<std::pair<std::string, std::string>>>&
          edge_relations,
      int concurrency) {
    int extra_vertex_label_num = vertex_tables_map.size();
    int total_vertex_label_num = vertex_label_num_ + extra_vertex_label_num;

    std::vector<std::shared_ptr<arrow::Table>> vertex_tables;
    vertex_tables.resize(extra_vertex_label_num);
    for (auto& pair : vertex_tables_map) {
      if (pair.first < vertex_label_num_ ||
          pair.first >= total_vertex_label_num) {
        RETURN_GS_ERROR(
            ErrorCode::kInvalidValueError,
            "Invalid vertex label id: " + std::to_string(pair.first));
      }
      vertex_tables[pair.first - vertex_label_num_] = pair.second;
    }
    int extra_edge_label_num = edge_tables_map.size();
    int total_edge_label_num = edge_label_num_ + extra_edge_label_num;

    std::vector<std::shared_ptr<arrow::Table>> edge_tables;
    edge_tables.resize(extra_edge_label_num);
    for (auto& pair : edge_tables_map) {
      if (pair.first < edge_label_num_ || pair.first >= total_edge_label_num) {
        RETURN_GS_ERROR(ErrorCode::kInvalidValueError,
                        "Invalid edge label id: " + std::to_string(pair.first));
      }
      edge_tables[pair.first - edge_label_num_] = pair.second;
    }
    return AddNewVertexEdgeLabels(client, std::move(vertex_tables),
                                  std::move(edge_tables), vm_id, edge_relations,
                                  concurrency);
  }

  boost::leaf::result<ObjectID> AddVertices(
      Client & client,
      std::map<label_id_t, std::shared_ptr<arrow::Table>> && vertex_tables_map,
      ObjectID vm_id) {
    int extra_vertex_label_num = vertex_tables_map.size();
    int total_vertex_label_num = vertex_label_num_ + extra_vertex_label_num;

    std::vector<std::shared_ptr<arrow::Table>> vertex_tables;
    vertex_tables.resize(extra_vertex_label_num);
    for (auto& pair : vertex_tables_map) {
      if (pair.first < vertex_label_num_ ||
          pair.first >= total_vertex_label_num) {
        RETURN_GS_ERROR(
            ErrorCode::kInvalidValueError,
            "Invalid vertex label id: " + std::to_string(pair.first));
      }
      vertex_tables[pair.first - vertex_label_num_] = pair.second;
    }
    return AddNewVertexLabels(client, std::move(vertex_tables), vm_id);
  }

  boost::leaf::result<ObjectID> AddEdges(
      Client & client,
      std::map<label_id_t, std::shared_ptr<arrow::Table>> && edge_tables_map,
      const std::vector<std::set<std::pair<std::string, std::string>>>&
          edge_relations,
      int concurrency) {
    int extra_edge_label_num = edge_tables_map.size();
    int total_edge_label_num = edge_label_num_ + extra_edge_label_num;

    std::vector<std::shared_ptr<arrow::Table>> edge_tables;
    edge_tables.resize(extra_edge_label_num);
    for (auto& pair : edge_tables_map) {
      if (pair.first < edge_label_num_ || pair.first >= total_edge_label_num) {
        RETURN_GS_ERROR(ErrorCode::kInvalidValueError,
                        "Invalid edge label id: " + std::to_string(pair.first));
      }
      edge_tables[pair.first - edge_label_num_] = pair.second;
    }
    return AddNewEdgeLabels(client, std::move(edge_tables), edge_relations,
                            concurrency);
  }

  /// Add a set of new vertex labels and a set of new edge labels to graph.
  /// Vertex label id started from vertex_label_num_, and edge label id
  /// started from edge_label_num_.
  boost::leaf::result<ObjectID> AddNewVertexEdgeLabels(
      Client & client,
      std::vector<std::shared_ptr<arrow::Table>> && vertex_tables,
      std::vector<std::shared_ptr<arrow::Table>> && edge_tables, ObjectID vm_id,
      const std::vector<std::set<std::pair<std::string, std::string>>>&
          edge_relations,
      int concurrency) {
    int extra_vertex_label_num = vertex_tables.size();
    int total_vertex_label_num = vertex_label_num_ + extra_vertex_label_num;
    int extra_edge_label_num = edge_tables.size();
    int total_edge_label_num = edge_label_num_ + extra_edge_label_num;

    // Init size
    auto vm_ptr =
        std::dynamic_pointer_cast<vertex_map_t>(client.GetObject(vm_id));

    std::vector<vid_t> ivnums(total_vertex_label_num);
    std::vector<vid_t> ovnums(total_vertex_label_num);
    std::vector<vid_t> tvnums(total_vertex_label_num);
    for (label_id_t i = 0; i < vertex_label_num_; ++i) {
      ivnums[i] = ivnums_[i];
    }
    for (size_t i = 0; i < vertex_tables.size(); ++i) {
      ARROW_OK_ASSIGN_OR_RAISE(
          vertex_tables[i],
          vertex_tables[i]->CombineChunks(arrow::default_memory_pool()));
      ivnums[vertex_label_num_ + i] =
          vm_ptr->GetInnerVertexSize(fid_, vertex_label_num_ + i);
    }

    // Collect extra outer vertices.
    auto collect_extra_outer_vertices =
        [this](const std::shared_ptr<vid_array_t>& gid_array,
               std::vector<std::vector<vid_t>>& extra_ovgids) {
          const VID_T* arr = gid_array->raw_values();
          for (int64_t i = 0; i < gid_array->length(); ++i) {
            fid_t fid = vid_parser_.GetFid(arr[i]);
            label_id_t label_id = vid_parser_.GetLabelId(arr[i]);
            bool flag = true;
            if (fid != fid_) {
              if (label_id < vertex_label_num_) {
                auto cur_map = ovg2l_maps_ptr_[label_id];
                flag = cur_map->find(arr[i]) == cur_map->end();
              }
            } else {
              flag = false;
            }

            if (flag) {
              extra_ovgids[label_id].push_back(arr[i]);
            }
          }
        };

    std::vector<std::vector<vid_t>> extra_ovgids(total_vertex_label_num);
    for (int i = 0; i < extra_edge_label_num; ++i) {
      ARROW_OK_ASSIGN_OR_RAISE(
          edge_tables[i],
          edge_tables[i]->CombineChunks(arrow::default_memory_pool()));

      collect_extra_outer_vertices(
          std::dynamic_pointer_cast<
              typename vineyard::ConvertToArrowType<vid_t>::ArrayType>(
              edge_tables[i]->column(0)->chunk(0)),
          extra_ovgids);
      collect_extra_outer_vertices(
          std::dynamic_pointer_cast<
              typename vineyard::ConvertToArrowType<vid_t>::ArrayType>(
              edge_tables[i]->column(1)->chunk(0)),
          extra_ovgids);
    }

    // Construct the new start value of lid of extra outer vertices
    std::vector<vid_t> start_ids(total_vertex_label_num);
    for (label_id_t i = 0; i < vertex_label_num_; ++i) {
      start_ids[i] = vid_parser_.GenerateId(0, i, ivnums_[i]) + ovnums_[i];
    }
    for (label_id_t i = vertex_label_num_; i < total_vertex_label_num; ++i) {
      start_ids[i] = vid_parser_.GenerateId(0, i, ivnums[i]);
    }

    // Make a copy of ovg2l map, since we need to add some extra outer vertices
    // pulled in this fragment by new edges.
    std::vector<ovg2l_map_t> ovg2l_maps(total_vertex_label_num);
    for (int i = 0; i < vertex_label_num_; ++i) {
      for (auto iter = ovg2l_maps_ptr_[i]->begin();
           iter != ovg2l_maps_ptr_[i]->end(); ++iter) {
        ovg2l_maps[i].emplace(iter->first, iter->second);
      }
    }

    std::vector<std::shared_ptr<vid_array_t>> extra_ovgid_lists(
        total_vertex_label_num);
    // Add extra outer vertices to ovg2l map, and collect distinct gid of extra
    // outer vertices.
    generate_outer_vertices_map(extra_ovgids, start_ids, total_vertex_label_num,
                                ovg2l_maps, extra_ovgid_lists);
    extra_ovgids.clear();

    std::vector<std::shared_ptr<vid_array_t>> ovgid_lists(
        total_vertex_label_num);
    // Append extra ovgid_lists with origin ovgid_lists to make it complete
    for (label_id_t i = 0; i < total_vertex_label_num; ++i) {
      vid_builder_t ovgid_list_builder;
      // If the ovgid have no new entries, leave it empty to indicate using the
      // old ovgid when seal.
      if (extra_ovgid_lists[i]->length() != 0) {
        if (i < vertex_label_num_) {
          ARROW_OK_OR_RAISE(ovgid_list_builder.AppendValues(
              ovgid_lists_[i]->raw_values(), ovgid_lists_[i]->length()));
        }
        ARROW_OK_OR_RAISE(
            ovgid_list_builder.AppendValues(extra_ovgid_lists[i]->raw_values(),
                                            extra_ovgid_lists[i]->length()));
      }
      ARROW_OK_OR_RAISE(ovgid_list_builder.Finish(&ovgid_lists[i]));

      ovnums[i] = i < vertex_label_num_ ? ovgid_lists_[i]->length() : 0;
      ovnums[i] += extra_ovgid_lists[i]->length();
      tvnums[i] = ivnums[i] + ovnums[i];
    }

    // Gather all local id of new edges.
    // And delete the src/dst column in edge tables.
    std::vector<std::shared_ptr<vid_array_t>> edge_src, edge_dst;
    edge_src.resize(extra_edge_label_num);
    edge_dst.resize(extra_edge_label_num);
    for (int i = 0; i < extra_edge_label_num; ++i) {
      generate_local_id_list(vid_parser_,
                             std::dynamic_pointer_cast<vid_array_t>(
                                 edge_tables[i]->column(0)->chunk(0)),
                             fid_, ovg2l_maps, concurrency, edge_src[i]);
      generate_local_id_list(vid_parser_,
                             std::dynamic_pointer_cast<vid_array_t>(
                                 edge_tables[i]->column(1)->chunk(0)),
                             fid_, ovg2l_maps, concurrency, edge_dst[i]);
      std::shared_ptr<arrow::Table> tmp_table0;
      ARROW_OK_ASSIGN_OR_RAISE(tmp_table0, edge_tables[i]->RemoveColumn(0));
      ARROW_OK_ASSIGN_OR_RAISE(edge_tables[i], tmp_table0->RemoveColumn(0));
    }

    // Generate CSR vector of new edge tables.

    std::vector<std::vector<std::shared_ptr<arrow::FixedSizeBinaryArray>>>
        ie_lists(total_vertex_label_num);
    std::vector<std::vector<std::shared_ptr<arrow::FixedSizeBinaryArray>>>
        oe_lists(total_vertex_label_num);
    std::vector<std::vector<std::shared_ptr<arrow::Int64Array>>>
        ie_offsets_lists(total_vertex_label_num);
    std::vector<std::vector<std::shared_ptr<arrow::Int64Array>>>
        oe_offsets_lists(total_vertex_label_num);

    for (label_id_t v_label = 0; v_label < total_vertex_label_num; ++v_label) {
      oe_lists[v_label].resize(total_edge_label_num);
      oe_offsets_lists[v_label].resize(total_edge_label_num);
      if (directed_) {
        ie_lists[v_label].resize(total_edge_label_num);
        ie_offsets_lists[v_label].resize(total_edge_label_num);
      }
    }

    for (label_id_t v_label = 0; v_label < vertex_label_num_; ++v_label) {
      for (label_id_t e_label = 0; e_label < edge_label_num_; ++e_label) {
        vid_t prev_offset_size = tvnums_[v_label] + 1;
        vid_t cur_offset_size = tvnums[v_label] + 1;
        if (directed_) {
          std::vector<int64_t> offsets(cur_offset_size);
          const int64_t* offset_array = ie_offsets_ptr_lists_[v_label][e_label];
          for (vid_t k = 0; k < prev_offset_size; ++k) {
            offsets[k] = offset_array[k];
          }
          for (vid_t k = prev_offset_size; k < cur_offset_size; ++k) {
            offsets[k] = offsets[k - 1];
          }
          arrow::Int64Builder builder;
          ARROW_OK_OR_RAISE(builder.AppendValues(offsets));
          ARROW_OK_OR_RAISE(
              builder.Finish(&ie_offsets_lists[v_label][e_label]));
        }
        std::vector<int64_t> offsets(cur_offset_size);
        const int64_t* offset_array = oe_offsets_ptr_lists_[v_label][e_label];
        for (size_t k = 0; k < prev_offset_size; ++k) {
          offsets[k] = offset_array[k];
        }
        for (size_t k = prev_offset_size; k < cur_offset_size; ++k) {
          offsets[k] = offsets[k - 1];
        }
        arrow::Int64Builder builder;
        ARROW_OK_OR_RAISE(builder.AppendValues(offsets));
        ARROW_OK_OR_RAISE(builder.Finish(&oe_offsets_lists[v_label][e_label]));
      }
    }

    for (label_id_t e_label = 0; e_label < total_edge_label_num; ++e_label) {
      std::vector<std::shared_ptr<arrow::FixedSizeBinaryArray>> sub_ie_lists(
          total_vertex_label_num);
      std::vector<std::shared_ptr<arrow::FixedSizeBinaryArray>> sub_oe_lists(
          total_vertex_label_num);
      std::vector<std::shared_ptr<arrow::Int64Array>> sub_ie_offset_lists(
          total_vertex_label_num);
      std::vector<std::shared_ptr<arrow::Int64Array>> sub_oe_offset_lists(
          total_vertex_label_num);

      // Process v_num...total_v_num  X  0...e_num  part.
      if (e_label < edge_label_num_) {
        if (directed_) {
          for (label_id_t v_label = vertex_label_num_;
               v_label < total_vertex_label_num; ++v_label) {
            PodArrayBuilder<nbr_unit_t> binary_builder;
            std::shared_ptr<arrow::FixedSizeBinaryArray> ie_array;
            ARROW_OK_OR_RAISE(binary_builder.Finish(&ie_array));

            sub_ie_lists[v_label] = ie_array;

            arrow::Int64Builder int64_builder;
            std::vector<int64_t> offset_vec(tvnums[v_label] + 1, 0);
            ARROW_OK_OR_RAISE(int64_builder.AppendValues(offset_vec));
            std::shared_ptr<arrow::Int64Array> ie_offset_array;
            ARROW_OK_OR_RAISE(int64_builder.Finish(&ie_offset_array));
            sub_ie_offset_lists[v_label] = ie_offset_array;
          }
        }
        for (label_id_t v_label = vertex_label_num_;
             v_label < total_vertex_label_num; ++v_label) {
          PodArrayBuilder<nbr_unit_t> binary_builder;
          std::shared_ptr<arrow::FixedSizeBinaryArray> oe_array;
          ARROW_OK_OR_RAISE(binary_builder.Finish(&oe_array));
          sub_oe_lists[v_label] = oe_array;

          arrow::Int64Builder int64_builder;
          std::vector<int64_t> offset_vec(tvnums[v_label] + 1, 0);
          ARROW_OK_OR_RAISE(int64_builder.AppendValues(offset_vec));
          std::shared_ptr<arrow::Int64Array> oe_offset_array;
          ARROW_OK_OR_RAISE(int64_builder.Finish(&oe_offset_array));
          sub_oe_offset_lists[v_label] = oe_offset_array;
        }
      } else {
        auto cur_label_index = e_label - edge_label_num_;
        // Process v_num...total_v_num  X  0...e_num  part.
        if (directed_) {
          // Process 0...total_v_num  X  e_num...total_e_num  part.
          generate_directed_csr<vid_t, eid_t>(
              vid_parser_, edge_src[cur_label_index], edge_dst[cur_label_index],
              tvnums, total_vertex_label_num, concurrency, sub_oe_lists,
              sub_oe_offset_lists, is_multigraph_);
          generate_directed_csr<vid_t, eid_t>(
              vid_parser_, edge_dst[cur_label_index], edge_src[cur_label_index],
              tvnums, total_vertex_label_num, concurrency, sub_ie_lists,
              sub_ie_offset_lists, is_multigraph_);
        } else {
          generate_undirected_csr<vid_t, eid_t>(
              vid_parser_, edge_src[cur_label_index], edge_dst[cur_label_index],
              tvnums, total_vertex_label_num, concurrency, sub_oe_lists,
              sub_oe_offset_lists, is_multigraph_);
        }
      }

      for (label_id_t v_label = 0; v_label < total_vertex_label_num;
           ++v_label) {
        if (v_label < vertex_label_num_ && e_label < edge_label_num_) {
          continue;
        }
        if (directed_) {
          ie_lists[v_label][e_label] = sub_ie_lists[v_label];
          ie_offsets_lists[v_label][e_label] = sub_ie_offset_lists[v_label];
        }
        oe_lists[v_label][e_label] = sub_oe_lists[v_label];
        oe_offsets_lists[v_label][e_label] = sub_oe_offset_lists[v_label];
      }
    }

    ArrowFragmentBaseBuilder<OID_T, VID_T> builder(*this);
    builder.set_vertex_label_num_(total_vertex_label_num);
    builder.set_edge_label_num_(total_edge_label_num);

    auto schema = schema_;  // make a copy

    // Extra vertex table
    for (label_id_t extra_label_id = 0; extra_label_id < extra_vertex_label_num;
         ++extra_label_id) {
      int label_id = vertex_label_num_ + extra_label_id;
      auto const& table = vertex_tables[extra_label_id];
      builder.set_vertex_tables_(label_id,
                                 TableBuilder(client, table).Seal(client));

      // build schema entry for the new vertex
      std::unordered_map<std::string, std::string> kvs;
      table->schema()->metadata()->ToUnorderedMap(&kvs);

      auto entry = schema.CreateEntry(kvs["label"], "VERTEX");
      for (auto const& field : table->fields()) {
        entry->AddProperty(field->name(), field->type());
      }
      std::string retain_oid = kvs["retain_oid"];
      if (retain_oid == "1" || retain_oid == "true") {
        int column_index = table->num_columns() - 1;
        entry->AddPrimaryKey(table->schema()->field(column_index)->name());
      }
    }

    // extra edge tables
    for (label_id_t extra_label_id = 0; extra_label_id < extra_edge_label_num;
         ++extra_label_id) {
      label_id_t label_id = edge_label_num_ + extra_label_id;
      auto const& table = edge_tables[extra_label_id];
      builder.set_edge_tables_(label_id,
                               TableBuilder(client, table).Seal(client));

      // build schema entry for the new edge
      std::unordered_map<std::string, std::string> kvs;
      table->schema()->metadata()->ToUnorderedMap(&kvs);
      auto entry = schema.CreateEntry(kvs["label"], "EDGE");
      for (auto const& field : table->fields()) {
        entry->AddProperty(field->name(), field->type());
      }
      for (const auto& rel : edge_relations[extra_label_id]) {
        entry->AddRelation(rel.first, rel.second);
      }
    }

    std::string error_message;
    if (!schema.Validate(error_message)) {
      RETURN_GS_ERROR(ErrorCode::kInvalidValueError, error_message);
    }
    builder.set_schema_json_(schema.ToJSON());

    ThreadGroup tg;
    {
      // ivnums, ovnums, tvnums
      auto fn = [this, &builder, &ivnums, &ovnums, &tvnums](Client& client) {
        vineyard::ArrayBuilder<vid_t> ivnums_builder(client, ivnums);
        vineyard::ArrayBuilder<vid_t> ovnums_builder(client, ovnums);
        vineyard::ArrayBuilder<vid_t> tvnums_builder(client, tvnums);
        builder.set_ivnums_(ivnums_builder.Seal(client));
        builder.set_ovnums_(ovnums_builder.Seal(client));
        builder.set_tvnums_(tvnums_builder.Seal(client));
        return Status::OK();
      };
      tg.AddTask(fn, std::ref(client));
    }

    // Extra ovgid, ovg2l
    //
    // If the map have no new entries, clear it to indicate using the old map
    // when seal.
    for (int i = 0; i < vertex_label_num_; ++i) {
      if (ovg2l_maps_ptr_[i]->size() == ovg2l_maps[i].size()) {
        ovg2l_maps[i].clear();
      }
    }
    for (label_id_t i = 0; i < total_vertex_label_num; ++i) {
      auto fn = [this, &builder, i, &ovgid_lists, &ovg2l_maps](Client& client) {
        if (i >= vertex_label_num_ || ovgid_lists[i]->length() != 0) {
          vineyard::NumericArrayBuilder<vid_t> ovgid_list_builder(
              client, ovgid_lists[i]);
          builder.set_ovgid_lists_(i, ovgid_list_builder.Seal(client));
        }

        if (i >= vertex_label_num_ || !ovg2l_maps[i].empty()) {
          vineyard::HashmapBuilder<vid_t, vid_t> ovg2l_builder(
              client, std::move(ovg2l_maps[i]));
          builder.set_ovg2l_maps_(i, ovg2l_builder.Seal(client));
        }
        return Status::OK();
      };
      tg.AddTask(fn, std::ref(client));
    }

    // Extra ie_list, oe_list, ie_offset_list, oe_offset_list
    for (label_id_t i = 0; i < total_vertex_label_num; ++i) {
      for (label_id_t j = 0; j < total_edge_label_num; ++j) {
        auto fn = [this, &builder, i, j, &ie_lists, &oe_lists,
                   &ie_offsets_lists, &oe_offsets_lists](Client& client) {
          if (directed_) {
            if (!(i < vertex_label_num_ && j < edge_label_num_)) {
              vineyard::FixedSizeBinaryArrayBuilder ie_builder(client,
                                                               ie_lists[i][j]);
              builder.set_ie_lists_(i, j, ie_builder.Seal(client));
            }
            vineyard::NumericArrayBuilder<int64_t> ieo_builder(
                client, ie_offsets_lists[i][j]);
            builder.set_ie_offsets_lists_(i, j, ieo_builder.Seal(client));
          }
          if (!(i < vertex_label_num_ && j < edge_label_num_)) {
            vineyard::FixedSizeBinaryArrayBuilder oe_builder(client,
                                                             oe_lists[i][j]);
            builder.set_oe_lists_(i, j, oe_builder.Seal(client));
          }
          vineyard::NumericArrayBuilder<int64_t> oeo_builder(
              client, oe_offsets_lists[i][j]);
          builder.set_oe_offsets_lists_(i, j, oeo_builder.Seal(client));
          return Status::OK();
        };
        tg.AddTask(fn, std::ref(client));
      }
    }

    // wait all
    tg.TakeResults();

    builder.set_vm_ptr_(vm_ptr);

    return builder.Seal(client)->id();
  }

  /// Add a set of new vertex labels to graph. Vertex label id started from
  /// vertex_label_num_.
  boost::leaf::result<ObjectID> AddNewVertexLabels(
      Client & client,
      std::vector<std::shared_ptr<arrow::Table>> && vertex_tables,
      ObjectID vm_id) {
    int extra_vertex_label_num = vertex_tables.size();
    int total_vertex_label_num = vertex_label_num_ + extra_vertex_label_num;

    auto vm_ptr =
        std::dynamic_pointer_cast<vertex_map_t>(client.GetObject(vm_id));

    std::vector<vid_t> ivnums(total_vertex_label_num);
    std::vector<vid_t> ovnums(total_vertex_label_num);
    std::vector<vid_t> tvnums(total_vertex_label_num);
    for (label_id_t i = 0; i < vertex_label_num_; ++i) {
      ivnums[i] = ivnums_[i];
      ovnums[i] = ovnums_[i];
      tvnums[i] = tvnums_[i];
    }
    for (size_t i = 0; i < vertex_tables.size(); ++i) {
      ARROW_OK_ASSIGN_OR_RAISE(
          vertex_tables[i],
          vertex_tables[i]->CombineChunks(arrow::default_memory_pool()));
      ivnums[vertex_label_num_ + i] =
          vm_ptr->GetInnerVertexSize(fid_, vertex_label_num_ + i);
      ovnums[vertex_label_num_ + i] = 0;
      tvnums[vertex_label_num_ + i] = ivnums[vertex_label_num_ + i];
    }

    ArrowFragmentBaseBuilder<OID_T, VID_T> builder(*this);
    builder.set_vertex_label_num_(total_vertex_label_num);

    auto schema = schema_;
    for (int extra_label_id = 0; extra_label_id < extra_vertex_label_num;
         ++extra_label_id) {
      int label_id = vertex_label_num_ + extra_label_id;
      auto const& table = vertex_tables[extra_label_id];
      builder.set_vertex_tables_(label_id,
                                 TableBuilder(client, table).Seal(client));

      // build schema entry for the new vertex
      std::unordered_map<std::string, std::string> kvs;
      table->schema()->metadata()->ToUnorderedMap(&kvs);

      auto entry = schema.CreateEntry(kvs["label"], "VERTEX");
      for (auto const& field : table->fields()) {
        entry->AddProperty(field->name(), field->type());
      }
      std::string retain_oid = kvs["retain_oid"];
      if (retain_oid == "1" || retain_oid == "true") {
        int col_id = table->num_columns() - 1;
        entry->AddPrimaryKey(table->schema()->field(col_id)->name());
      }
    }
    std::string error_message;
    if (!schema.Validate(error_message)) {
      RETURN_GS_ERROR(ErrorCode::kInvalidValueError, error_message);
    }
    builder.set_schema_json_(schema.ToJSON());

    vineyard::ArrayBuilder<vid_t> ivnums_builder(client, ivnums);
    vineyard::ArrayBuilder<vid_t> ovnums_builder(client, ovnums);
    vineyard::ArrayBuilder<vid_t> tvnums_builder(client, tvnums);

    builder.set_ivnums_(ivnums_builder.Seal(client));
    builder.set_ovnums_(ovnums_builder.Seal(client));
    builder.set_tvnums_(tvnums_builder.Seal(client));

    // Assign additional meta for new vertex labels
    std::vector<std::vector<std::shared_ptr<vineyard::FixedSizeBinaryArray>>>
        vy_ie_lists, vy_oe_lists;
    std::vector<std::vector<std::shared_ptr<vineyard::NumericArray<int64_t>>>>
        vy_ie_offsets_lists, vy_oe_offsets_lists;

    for (label_id_t extra_label_id = 0; extra_label_id < extra_vertex_label_num;
         ++extra_label_id) {
      label_id_t label_id = vertex_label_num_ + extra_label_id;
      vineyard::NumericArrayBuilder<vid_t> ovgid_list_builder(client);
      builder.set_ovgid_lists_(label_id, ovgid_list_builder.Seal(client));

      vineyard::HashmapBuilder<vid_t, vid_t> ovg2l_builder(client);
      builder.set_ovg2l_maps_(label_id, ovg2l_builder.Seal(client));
    }

    for (label_id_t i = 0; i < extra_vertex_label_num; ++i) {
      for (label_id_t j = 0; j < edge_label_num_; ++j) {
        label_id_t vertex_label_id = vertex_label_num_ + i;
        if (directed_) {
          vineyard::FixedSizeBinaryArrayBuilder ie_builder(
              client, arrow::fixed_size_binary(sizeof(nbr_unit_t)));
          builder.set_ie_lists_(vertex_label_id, j, ie_builder.Seal(client));

          arrow::Int64Builder int64_builder;
          // Offset vector's length is tvnum + 1
          std::vector<int64_t> offset_vec(tvnums[vertex_label_id] + 1, 0);
          ARROW_OK_OR_RAISE(int64_builder.AppendValues(offset_vec));
          std::shared_ptr<arrow::Int64Array> ie_offset_array;
          ARROW_OK_OR_RAISE(int64_builder.Finish(&ie_offset_array));

          vineyard::NumericArrayBuilder<int64_t> ie_offset_builder(
              client, ie_offset_array);
          builder.set_ie_offsets_lists_(vertex_label_id, j,
                                        ie_offset_builder.Seal(client));
        }

        vineyard::FixedSizeBinaryArrayBuilder oe_builder(
            client, arrow::fixed_size_binary(sizeof(nbr_unit_t)));
        builder.set_oe_lists_(vertex_label_id, j, oe_builder.Seal(client));

        arrow::Int64Builder int64_builder;
        // Offset vector's length is tvnum + 1
        std::vector<int64_t> offset_vec(tvnums[vertex_label_id] + 1, 0);
        ARROW_OK_OR_RAISE(int64_builder.AppendValues(offset_vec));
        std::shared_ptr<arrow::Int64Array> oe_offset_array;
        ARROW_OK_OR_RAISE(int64_builder.Finish(&oe_offset_array));
        vineyard::NumericArrayBuilder<int64_t> oe_offset_builder(
            client, oe_offset_array);
        builder.set_oe_offsets_lists_(vertex_label_id, j,
                                      oe_offset_builder.Seal(client));
      }
    }

    builder.set_vm_ptr_(vm_ptr);
    return builder.Seal(client)->id();
  }

  /// Add a set of new edge labels to graph. Edge label id started from
  /// edge_label_num_.
  boost::leaf::result<ObjectID> AddNewEdgeLabels(
      Client & client,
      std::vector<std::shared_ptr<arrow::Table>> && edge_tables,
      const std::vector<std::set<std::pair<std::string, std::string>>>&
          edge_relations,
      int concurrency) {
    int extra_edge_label_num = edge_tables.size();
    int total_edge_label_num = edge_label_num_ + extra_edge_label_num;

    // Collect extra outer vertices.
    auto collect_extra_outer_vertices =
        [this](const std::shared_ptr<vid_array_t>& gid_array,
               std::vector<std::vector<vid_t>>& extra_ovgids) {
          const VID_T* arr = gid_array->raw_values();
          for (int64_t i = 0; i < gid_array->length(); ++i) {
            fid_t fid = vid_parser_.GetFid(arr[i]);
            label_id_t label_id = vid_parser_.GetLabelId(arr[i]);
            auto cur_map = ovg2l_maps_ptr_[label_id];
            if (fid != fid_ && cur_map->find(arr[i]) == cur_map->end()) {
              extra_ovgids[vid_parser_.GetLabelId(arr[i])].push_back(arr[i]);
            }
          }
        };

    std::vector<std::vector<vid_t>> extra_ovgids(vertex_label_num_);
    for (int i = 0; i < extra_edge_label_num; ++i) {
      ARROW_OK_ASSIGN_OR_RAISE(
          edge_tables[i],
          edge_tables[i]->CombineChunks(arrow::default_memory_pool()));

      collect_extra_outer_vertices(
          std::dynamic_pointer_cast<
              typename vineyard::ConvertToArrowType<vid_t>::ArrayType>(
              edge_tables[i]->column(0)->chunk(0)),
          extra_ovgids);
      collect_extra_outer_vertices(
          std::dynamic_pointer_cast<
              typename vineyard::ConvertToArrowType<vid_t>::ArrayType>(
              edge_tables[i]->column(1)->chunk(0)),
          extra_ovgids);
    }

    // Construct the new start value of lid of extra outer vertices
    std::vector<vid_t> start_ids(vertex_label_num_);
    for (label_id_t i = 0; i < vertex_label_num_; ++i) {
      start_ids[i] = vid_parser_.GenerateId(0, i, ivnums_[i]) + ovnums_[i];
    }

    // Make a copy of ovg2l map, since we need to add some extra outer vertices
    // pulled in this fragment by new edges.
    std::vector<ovg2l_map_t> ovg2l_maps(vertex_label_num_);
    for (int i = 0; i < vertex_label_num_; ++i) {
      for (auto iter = ovg2l_maps_ptr_[i]->begin();
           iter != ovg2l_maps_ptr_[i]->end(); ++iter) {
        ovg2l_maps[i].emplace(iter->first, iter->second);
      }
    }

    std::vector<std::shared_ptr<vid_array_t>> extra_ovgid_lists(
        vertex_label_num_);
    // Add extra outer vertices to ovg2l map, and collect distinct gid of extra
    // outer vertices.
    generate_outer_vertices_map(extra_ovgids, start_ids, vertex_label_num_,
                                ovg2l_maps, extra_ovgid_lists);
    extra_ovgids.clear();

    std::vector<vid_t> ovnums(vertex_label_num_), tvnums(vertex_label_num_);
    std::vector<std::shared_ptr<vid_array_t>> ovgid_lists(vertex_label_num_);
    // Append extra ovgid_lists with origin ovgid_lists to make it complete
    for (label_id_t i = 0; i < vertex_label_num_; ++i) {
      vid_builder_t ovgid_list_builder;
      // If the ovgid have no new entries, leave it empty to indicate using the
      // old ovgid when seal.
      if (extra_ovgid_lists[i]->length() != 0) {
        ARROW_OK_OR_RAISE(ovgid_list_builder.AppendValues(
            ovgid_lists_[i]->raw_values(), ovgid_lists_[i]->length()));
        ARROW_OK_OR_RAISE(
            ovgid_list_builder.AppendValues(extra_ovgid_lists[i]->raw_values(),
                                            extra_ovgid_lists[i]->length()));
      }
      ARROW_OK_OR_RAISE(ovgid_list_builder.Finish(&ovgid_lists[i]));

      ovnums[i] = ovgid_lists_[i]->length() + extra_ovgid_lists[i]->length();
      tvnums[i] = ivnums_[i] + ovnums[i];
    }

    std::vector<std::vector<std::shared_ptr<arrow::Int64Array>>>
        ie_offsets_lists_expanded(vertex_label_num_);
    std::vector<std::vector<std::shared_ptr<arrow::Int64Array>>>
        oe_offsets_lists_expanded(vertex_label_num_);

    for (label_id_t v_label = 0; v_label < vertex_label_num_; ++v_label) {
      if (directed_) {
        ie_offsets_lists_expanded[v_label].resize(edge_label_num_);
      }
      oe_offsets_lists_expanded[v_label].resize(edge_label_num_);
    }
    for (label_id_t v_label = 0; v_label < vertex_label_num_; ++v_label) {
      for (label_id_t e_label = 0; e_label < edge_label_num_; ++e_label) {
        vid_t prev_offset_size = tvnums_[v_label] + 1;
        vid_t cur_offset_size = tvnums[v_label] + 1;
        if (directed_) {
          std::vector<int64_t> offsets(cur_offset_size);
          const int64_t* offset_array = ie_offsets_ptr_lists_[v_label][e_label];
          for (vid_t k = 0; k < prev_offset_size; ++k) {
            offsets[k] = offset_array[k];
          }
          for (vid_t k = prev_offset_size; k < cur_offset_size; ++k) {
            offsets[k] = offsets[k - 1];
          }
          arrow::Int64Builder builder;
          ARROW_OK_OR_RAISE(builder.AppendValues(offsets));
          ARROW_OK_OR_RAISE(
              builder.Finish(&ie_offsets_lists_expanded[v_label][e_label]));
        }
        std::vector<int64_t> offsets(cur_offset_size);
        const int64_t* offset_array = oe_offsets_ptr_lists_[v_label][e_label];
        for (size_t k = 0; k < prev_offset_size; ++k) {
          offsets[k] = offset_array[k];
        }
        for (size_t k = prev_offset_size; k < cur_offset_size; ++k) {
          offsets[k] = offsets[k - 1];
        }
        arrow::Int64Builder builder;
        ARROW_OK_OR_RAISE(builder.AppendValues(offsets));
        ARROW_OK_OR_RAISE(
            builder.Finish(&oe_offsets_lists_expanded[v_label][e_label]));
      }
    }
    // Gather all local id of new edges.
    // And delete the src/dst column in edge tables.
    std::vector<std::shared_ptr<vid_array_t>> edge_src, edge_dst;
    edge_src.resize(extra_edge_label_num);
    edge_dst.resize(extra_edge_label_num);
    for (int i = 0; i < extra_edge_label_num; ++i) {
      generate_local_id_list(vid_parser_,
                             std::dynamic_pointer_cast<vid_array_t>(
                                 edge_tables[i]->column(0)->chunk(0)),
                             fid_, ovg2l_maps, concurrency, edge_src[i]);
      generate_local_id_list(vid_parser_,
                             std::dynamic_pointer_cast<vid_array_t>(
                                 edge_tables[i]->column(1)->chunk(0)),
                             fid_, ovg2l_maps, concurrency, edge_dst[i]);
      std::shared_ptr<arrow::Table> tmp_table0;
      ARROW_OK_ASSIGN_OR_RAISE(tmp_table0, edge_tables[i]->RemoveColumn(0));
      ARROW_OK_ASSIGN_OR_RAISE(edge_tables[i], tmp_table0->RemoveColumn(0));
    }

    // Generate CSR vector of new edge tables.

    std::vector<std::vector<std::shared_ptr<arrow::FixedSizeBinaryArray>>>
        ie_lists(vertex_label_num_);
    std::vector<std::vector<std::shared_ptr<arrow::FixedSizeBinaryArray>>>
        oe_lists(vertex_label_num_);
    std::vector<std::vector<std::shared_ptr<arrow::Int64Array>>>
        ie_offsets_lists(vertex_label_num_);
    std::vector<std::vector<std::shared_ptr<arrow::Int64Array>>>
        oe_offsets_lists(vertex_label_num_);

    for (label_id_t v_label = 0; v_label < vertex_label_num_; ++v_label) {
      oe_lists[v_label].resize(extra_edge_label_num);
      oe_offsets_lists[v_label].resize(extra_edge_label_num);
      if (directed_) {
        ie_lists[v_label].resize(extra_edge_label_num);
        ie_offsets_lists[v_label].resize(extra_edge_label_num);
      }
    }

    for (label_id_t e_label = 0; e_label < extra_edge_label_num; ++e_label) {
      std::vector<std::shared_ptr<arrow::FixedSizeBinaryArray>> sub_ie_lists(
          vertex_label_num_);
      std::vector<std::shared_ptr<arrow::FixedSizeBinaryArray>> sub_oe_lists(
          vertex_label_num_);
      std::vector<std::shared_ptr<arrow::Int64Array>> sub_ie_offset_lists(
          vertex_label_num_);
      std::vector<std::shared_ptr<arrow::Int64Array>> sub_oe_offset_lists(
          vertex_label_num_);
      if (directed_) {
        generate_directed_csr<vid_t, eid_t>(
            vid_parser_, edge_src[e_label], edge_dst[e_label], tvnums,
            vertex_label_num_, concurrency, sub_oe_lists, sub_oe_offset_lists,
            is_multigraph_);
        generate_directed_csr<vid_t, eid_t>(
            vid_parser_, edge_dst[e_label], edge_src[e_label], tvnums,
            vertex_label_num_, concurrency, sub_ie_lists, sub_ie_offset_lists,
            is_multigraph_);
      } else {
        generate_undirected_csr<vid_t, eid_t>(
            vid_parser_, edge_src[e_label], edge_dst[e_label], tvnums,
            vertex_label_num_, concurrency, sub_oe_lists, sub_oe_offset_lists,
            is_multigraph_);
      }

      for (label_id_t v_label = 0; v_label < vertex_label_num_; ++v_label) {
        if (directed_) {
          ie_lists[v_label][e_label] = sub_ie_lists[v_label];
          ie_offsets_lists[v_label][e_label] = sub_ie_offset_lists[v_label];
        }
        oe_lists[v_label][e_label] = sub_oe_lists[v_label];
        oe_offsets_lists[v_label][e_label] = sub_oe_offset_lists[v_label];
      }
    }

    ArrowFragmentBaseBuilder<OID_T, VID_T> builder(*this);
    builder.set_edge_label_num_(total_edge_label_num);

    auto schema = schema_;
    for (label_id_t extra_label_id = 0; extra_label_id < extra_edge_label_num;
         ++extra_label_id) {
      label_id_t label_id = edge_label_num_ + extra_label_id;
      auto const& table = edge_tables[extra_label_id];

      builder.set_edge_tables_(label_id,
                               TableBuilder(client, table).Seal(client));

      // build schema entry for the new edge
      std::unordered_map<std::string, std::string> kvs;
      table->schema()->metadata()->ToUnorderedMap(&kvs);
      auto entry = schema.CreateEntry(kvs["label"], "EDGE");
      for (auto const& field : table->fields()) {
        entry->AddProperty(field->name(), field->type());
      }
      for (const auto& rel : edge_relations[extra_label_id]) {
        entry->AddRelation(rel.first, rel.second);
      }
    }

    std::string error_message;
    if (!schema.Validate(error_message)) {
      RETURN_GS_ERROR(ErrorCode::kInvalidValueError, error_message);
    }
    builder.set_schema_json_(schema.ToJSON());

    ThreadGroup tg;
    {
      auto fn = [this, &builder, &ovnums, &tvnums](Client& client) {
        vineyard::ArrayBuilder<vid_t> ovnums_builder(client, ovnums);
        vineyard::ArrayBuilder<vid_t> tvnums_builder(client, tvnums);
        builder.set_ovnums_(ovnums_builder.Seal(client));
        builder.set_tvnums_(tvnums_builder.Seal(client));
        return Status::OK();
      };
      tg.AddTask(fn, std::ref(client));
    }

    // If the map have no new entries, clear it to indicate using the old map
    // when seal.
    for (int i = 0; i < vertex_label_num_; ++i) {
      if (ovg2l_maps_ptr_[i]->size() == ovg2l_maps[i].size()) {
        ovg2l_maps[i].clear();
      }
    }
    for (label_id_t i = 0; i < vertex_label_num_; ++i) {
      auto fn = [this, &builder, i, &ovgid_lists, &ovg2l_maps](Client& client) {
        if (ovgid_lists[i]->length() != 0) {
          vineyard::NumericArrayBuilder<vid_t> ovgid_list_builder(
              client, ovgid_lists[i]);
          builder.set_ovgid_lists_(i, ovgid_list_builder.Seal(client));
        }

        if (!ovg2l_maps[i].empty()) {
          vineyard::HashmapBuilder<vid_t, vid_t> ovg2l_builder(
              client, std::move(ovg2l_maps[i]));
          builder.set_ovg2l_maps_(i, ovg2l_builder.Seal(client));
        }
        return Status::OK();
      };
      tg.AddTask(fn, std::ref(client));
    }

    // Extra ie_list, oe_list, ie_offset_list, oe_offset_list
    for (label_id_t i = 0; i < vertex_label_num_; ++i) {
      for (label_id_t j = 0; j < extra_edge_label_num; ++j) {
        auto fn = [this, &builder, i, j, &ie_lists, &oe_lists,
                   &ie_offsets_lists, &oe_offsets_lists](Client& client) {
          label_id_t edge_label_id = edge_label_num_ + j;
          if (directed_) {
            vineyard::FixedSizeBinaryArrayBuilder ie_builder(client,
                                                             ie_lists[i][j]);
            builder.set_ie_lists_(i, edge_label_id, ie_builder.Seal(client));

            vineyard::NumericArrayBuilder<int64_t> ieo_builder(
                client, ie_offsets_lists[i][j]);
            builder.set_ie_offsets_lists_(i, edge_label_id,
                                          ieo_builder.Seal(client));
          }
          vineyard::FixedSizeBinaryArrayBuilder oe_builder(client,
                                                           oe_lists[i][j]);
          builder.set_oe_lists_(i, edge_label_id, oe_builder.Seal(client));

          vineyard::NumericArrayBuilder<int64_t> oeo_builder(
              client, oe_offsets_lists[i][j]);
          builder.set_oe_offsets_lists_(i, edge_label_id,
                                        oeo_builder.Seal(client));
          return Status::OK();
        };
        tg.AddTask(fn, std::ref(client));
      }
    }
    for (label_id_t i = 0; i < vertex_label_num_; ++i) {
      for (label_id_t j = 0; j < edge_label_num_; ++j) {
        auto fn = [this, &builder, i, j, &ie_offsets_lists_expanded,
                   &oe_offsets_lists_expanded](Client& client) {
          label_id_t edge_label_id = j;
          if (directed_) {
            vineyard::NumericArrayBuilder<int64_t> ieo_builder_expanded(
                client, ie_offsets_lists_expanded[i][j]);
            builder.set_ie_offsets_lists_(i, edge_label_id,
                                          ieo_builder_expanded.Seal(client));
          }
          vineyard::NumericArrayBuilder<int64_t> oeo_builder_expanded(
              client, oe_offsets_lists_expanded[i][j]);
          builder.set_oe_offsets_lists_(i, edge_label_id,
                                        oeo_builder_expanded.Seal(client));
          return Status::OK();
        };
        tg.AddTask(fn, std::ref(client));
      }
    }
    tg.TakeResults();

    return builder.Seal(client)->id();
  }

  boost::leaf::result<vineyard::ObjectID> AddVertexColumns(
      vineyard::Client & client,
      const std::map<
          label_id_t,
          std::vector<std::pair<std::string, std::shared_ptr<arrow::Array>>>>
          columns,
      bool replace = false) override {
    return AddVertexColumnsImpl<arrow::Array>(client, columns, replace);
  }

  boost::leaf::result<vineyard::ObjectID> AddVertexColumns(
      vineyard::Client & client,
      const std::map<label_id_t,
                     std::vector<std::pair<
                         std::string, std::shared_ptr<arrow::ChunkedArray>>>>
          columns,
      bool replace = false) override {
    return AddVertexColumnsImpl<arrow::ChunkedArray>(client, columns, replace);
  }

  template <typename ArrayType = arrow::Array>
  boost::leaf::result<vineyard::ObjectID> AddVertexColumnsImpl(
      vineyard::Client & client,
      const std::map<
          label_id_t,
          std::vector<std::pair<std::string, std::shared_ptr<ArrayType>>>>
          columns,
      bool replace = false) {
    ArrowFragmentBaseBuilder<OID_T, VID_T> builder(*this);

    auto schema = schema_;

    /// If replace == true, invalidate all previous properties that have new
    /// columns.
    if (replace) {
      for (auto& pair : columns) {
        auto label_id = pair.first;
        auto& entry = schema.GetMutableEntry(label_id, "VERTEX");
        for (size_t i = 0; i < entry.props_.size(); ++i) {
          entry.InvalidateProperty(i);
        }
      }
    }

    for (label_id_t label_id = 0; label_id < vertex_label_num_; ++label_id) {
      std::string table_name =
          generate_name_with_suffix("vertex_tables", label_id);
      if (columns.find(label_id) != columns.end()) {
        auto& table = this->vertex_tables_[label_id];
        vineyard::TableExtender extender(client, table);

        auto& vec = columns.at(label_id);
        for (auto& pair : vec) {
          auto status = extender.AddColumn(client, pair.first, pair.second);
          CHECK(status.ok());
        }
        auto new_table =
            std::dynamic_pointer_cast<vineyard::Table>(extender.Seal(client));
        builder.set_vertex_tables_(label_id, new_table);
        auto& entry = schema.GetMutableEntry(
            schema.GetVertexLabelName(label_id), "VERTEX");
        for (size_t index = table->num_columns();
             index < new_table->num_columns(); ++index) {
          entry.AddProperty(new_table->field(index)->name(),
                            new_table->field(index)->type());
        }
      }
    }
    std::string error_message;
    if (!schema.Validate(error_message)) {
      RETURN_GS_ERROR(ErrorCode::kInvalidValueError, error_message);
    }
    builder.set_schema_json_(schema.ToJSON());
    return builder.Seal(client)->id();
  }

  boost::leaf::result<vineyard::ObjectID> Project(
      vineyard::Client & client,
      std::map<label_id_t, std::vector<label_id_t>> vertices,
      std::map<label_id_t, std::vector<label_id_t>> edges) {
    ArrowFragmentBaseBuilder<OID_T, VID_T> builder(*this);

    auto schema = schema_;

    std::vector<label_id_t> vertex_labels, edge_labels;
    std::vector<std::vector<prop_id_t>> vertex_properties, edge_properties;

    for (auto& pair : vertices) {
      vertex_labels.push_back(pair.first);
      vertex_properties.push_back(pair.second);
    }
    for (auto& pair : edges) {
      edge_labels.push_back(pair.first);
      edge_properties.push_back(pair.second);
    }

    auto remove_invalid_relation =
        [&schema](const std::vector<label_id_t>& edge_labels,
                  std::map<label_id_t, std::vector<label_id_t>> vertices) {
          std::string type = "EDGE";
          for (size_t i = 0; i < edge_labels.size(); ++i) {
            auto& entry = schema.GetMutableEntry(edge_labels[i], type);
            auto& relations = entry.relations;
            std::vector<std::pair<std::string, std::string>> valid_relations;
            for (auto& pair : relations) {
              auto src = schema.GetVertexLabelId(pair.first);
              auto dst = schema.GetVertexLabelId(pair.second);
              if (vertices.find(src) != vertices.end() &&
                  vertices.find(dst) != vertices.end()) {
                valid_relations.push_back(pair);
              }
            }
            entry.relations = valid_relations;
          }
        };
    // Compute the set difference of reserved labels and all labels.
    auto invalidate_label = [&schema](const std::vector<label_id_t>& labels,
                                      std::string type, size_t label_num) {
      auto it = labels.begin();
      for (size_t i = 0; i < label_num; ++i) {
        if (it == labels.end() || i < *it) {
          if (type == "VERTEX") {
            schema.InvalidateVertex(i);
          } else {
            schema.InvalidateEdge(i);
          }
        } else {
          ++it;
        }
      }
    };

    auto invalidate_prop =
        [&schema](const std::vector<label_id_t>& labels, std::string type,
                  const std::vector<std::vector<prop_id_t>>& props) {
          for (size_t i = 0; i < labels.size(); ++i) {
            auto& entry = schema.GetMutableEntry(labels[i], type);
            auto it1 = props[i].begin();
            auto it2 = props[i].end();
            size_t prop_num = entry.props_.size();
            for (size_t j = 0; j < prop_num; ++j) {
              if (it1 == it2 || j < *it1) {
                entry.InvalidateProperty(j);
              } else {
                ++it1;
              }
            }
          }
        };
    remove_invalid_relation(edge_labels, vertices);
    invalidate_prop(vertex_labels, "VERTEX", vertex_properties);
    invalidate_prop(edge_labels, "EDGE", edge_properties);
    invalidate_label(vertex_labels, "VERTEX", schema.vertex_entries().size());
    invalidate_label(edge_labels, "EDGE", schema.edge_entries().size());

    std::string error_message;
    if (!schema.Validate(error_message)) {
      RETURN_GS_ERROR(ErrorCode::kInvalidValueError, error_message);
    }
    builder.set_schema_json_(schema.ToJSON());
    return builder.Seal(client)->id();
  }

  boost::leaf::result<vineyard::ObjectID> TransformDirection(
      vineyard::Client & client, int concurrency) {
    ArrowFragmentBaseBuilder<OID_T, VID_T> builder(*this);
    builder.set_directed_(!directed_);

    std::vector<std::vector<std::shared_ptr<arrow::FixedSizeBinaryArray>>>
        oe_lists(vertex_label_num_);
    std::vector<std::vector<std::shared_ptr<arrow::Int64Array>>>
        oe_offsets_lists(vertex_label_num_);

    for (label_id_t v_label = 0; v_label < vertex_label_num_; ++v_label) {
      oe_lists[v_label].resize(edge_label_num_);
      oe_offsets_lists[v_label].resize(edge_label_num_);
    }

    if (directed_) {
      bool is_multigraph = is_multigraph_;
      directedCSR2Undirected(oe_lists, oe_offsets_lists, concurrency,
                             is_multigraph);

      for (label_id_t i = 0; i < vertex_label_num_; ++i) {
        for (label_id_t j = 0; j < edge_label_num_; ++j) {
          vineyard::FixedSizeBinaryArrayBuilder oe_builder(client,
                                                           oe_lists[i][j]);
          builder.set_oe_lists_(i, j, oe_builder.Seal(client));

          vineyard::NumericArrayBuilder<int64_t> oeo_builder(
              client, oe_offsets_lists[i][j]);
          builder.set_oe_offsets_lists_(i, j, oeo_builder.Seal(client));
        }
      }
      builder.set_is_multigraph_(is_multigraph);
    }

    return builder.Seal(client)->id();
  }

 private:
  void initPointers() {
    edge_tables_columns_.resize(edge_label_num_);
    flatten_edge_tables_columns_.resize(edge_label_num_);
    for (label_id_t i = 0; i < edge_label_num_; ++i) {
      prop_id_t prop_num =
          static_cast<prop_id_t>(edge_tables_[i]->num_columns());
      edge_tables_columns_[i].resize(prop_num);
      if (edge_tables_[i]->num_rows() == 0) {
        continue;
      }
      for (prop_id_t j = 0; j < prop_num; ++j) {
        edge_tables_columns_[i][j] =
            get_arrow_array_data(edge_tables_[i]->column(j)->chunk(0));
      }
      flatten_edge_tables_columns_[i] = &edge_tables_columns_[i][0];
    }

    vertex_tables_columns_.resize(vertex_label_num_);
    for (label_id_t i = 0; i < vertex_label_num_; ++i) {
      auto vertex_table = vertex_tables_[i]->GetTable();
      prop_id_t prop_num = static_cast<prop_id_t>(vertex_table->num_columns());
      vertex_tables_columns_[i].resize(prop_num);
      if (vertex_table->num_rows() == 0) {
        continue;
      }
      for (prop_id_t j = 0; j < prop_num; ++j) {
        vertex_tables_columns_[i][j] =
            get_arrow_array_data(vertex_table->column(j)->chunk(0));
      }
    }

    oe_ptr_lists_.resize(vertex_label_num_);
    oe_offsets_ptr_lists_.resize(vertex_label_num_);

    idst_.resize(vertex_label_num_);
    odst_.resize(vertex_label_num_);
    iodst_.resize(vertex_label_num_);

    idoffset_.resize(vertex_label_num_);
    odoffset_.resize(vertex_label_num_);
    iodoffset_.resize(vertex_label_num_);

    ovgid_lists_ptr_.resize(vertex_label_num_);
    ovg2l_maps_ptr_.resize(vertex_label_num_);
    for (label_id_t i = 0; i < vertex_label_num_; ++i) {
      ovgid_lists_ptr_[i] = ovgid_lists_[i]->GetArray()->raw_values();
      ovg2l_maps_ptr_[i] = ovg2l_maps_[i].get();

      oe_ptr_lists_[i].resize(edge_label_num_);
      oe_offsets_ptr_lists_[i].resize(edge_label_num_);

      idst_[i].resize(edge_label_num_);
      odst_[i].resize(edge_label_num_);
      iodst_[i].resize(edge_label_num_);

      idoffset_[i].resize(edge_label_num_);
      odoffset_[i].resize(edge_label_num_);
      iodoffset_[i].resize(edge_label_num_);

      for (label_id_t j = 0; j < edge_label_num_; ++j) {
        oe_ptr_lists_[i][j] = reinterpret_cast<const nbr_unit_t*>(
            oe_lists_[i][j]->GetArray()->raw_values());
        oe_offsets_ptr_lists_[i][j] =
            oe_offsets_lists_[i][j]->GetArray()->raw_values();
      }
    }

    if (directed_) {
      ie_ptr_lists_.resize(vertex_label_num_);
      ie_offsets_ptr_lists_.resize(vertex_label_num_);
      for (label_id_t i = 0; i < vertex_label_num_; ++i) {
        ie_ptr_lists_[i].resize(edge_label_num_);
        ie_offsets_ptr_lists_[i].resize(edge_label_num_);
        for (label_id_t j = 0; j < edge_label_num_; ++j) {
          ie_ptr_lists_[i][j] = reinterpret_cast<const nbr_unit_t*>(
              ie_lists_[i][j]->GetArray()->raw_values());
          ie_offsets_ptr_lists_[i][j] =
              ie_offsets_lists_[i][j]->GetArray()->raw_values();
        }
      }
    } else {
      ie_ptr_lists_ = oe_ptr_lists_;
      ie_offsets_ptr_lists_ = oe_offsets_ptr_lists_;
    }
  }

  void initDestFidList(
      bool in_edge, bool out_edge,
      std::vector<std::vector<std::vector<fid_t>>>& fid_lists,
      std::vector<std::vector<std::vector<fid_t*>>>& fid_lists_offset) {
    for (auto v_label_id = 0; v_label_id < vertex_label_num_; v_label_id++) {
      auto ivnum_ = ivnums_[v_label_id];
      auto inner_vertices = InnerVertices(v_label_id);

      for (auto e_label_id = 0; e_label_id < edge_label_num_; e_label_id++) {
        std::vector<int> id_num(ivnum_, 0);
        std::set<fid_t> dstset;
        vertex_t v = *inner_vertices.begin();
        auto& fid_list = fid_lists[v_label_id][e_label_id];
        auto& fid_list_offset = fid_lists_offset[v_label_id][e_label_id];

        if (!fid_list_offset.empty()) {
          return;
        }
        fid_list_offset.resize(ivnum_ + 1, NULL);
        for (vid_t i = 0; i < ivnum_; ++i) {
          dstset.clear();
          if (in_edge) {
            auto es = GetIncomingAdjList(v, e_label_id);
            for (auto& e : es) {
              fid_t f = GetFragId(e.neighbor());
              if (f != fid_) {
                dstset.insert(f);
              }
            }
          }
          if (out_edge) {
            auto es = GetOutgoingAdjList(v, e_label_id);
            for (auto& e : es) {
              fid_t f = GetFragId(e.neighbor());
              if (f != fid_) {
                dstset.insert(f);
              }
            }
          }
          id_num[i] = dstset.size();
          for (auto fid : dstset) {
            fid_list.push_back(fid);
          }
          ++v;
        }

        fid_list.shrink_to_fit();
        fid_list_offset[0] = fid_list.data();
        for (vid_t i = 0; i < ivnum_; ++i) {
          fid_list_offset[i + 1] = fid_list_offset[i] + id_num[i];
        }
      }
    }
  }

  void directedCSR2Undirected(
      std::vector<std::vector<std::shared_ptr<arrow::FixedSizeBinaryArray>>> &
          oe_lists,
      std::vector<std::vector<std::shared_ptr<arrow::Int64Array>>> &
          oe_offsets_lists,
      int concurrency, bool& is_multigraph) {
    for (label_id_t v_label = 0; v_label < vertex_label_num_; ++v_label) {
      for (label_id_t e_label = 0; e_label < edge_label_num_; ++e_label) {
        const nbr_unit_t* ie = ie_ptr_lists_.at(v_label).at(e_label);
        const nbr_unit_t* oe = oe_ptr_lists_.at(v_label).at(e_label);
        const int64_t* ie_offset =
            ie_offsets_ptr_lists_.at(v_label).at(e_label);
        const int64_t* oe_offset =
            oe_offsets_ptr_lists_.at(v_label).at(e_label);

        // Merge edges from two array into one
        vineyard::PodArrayBuilder<nbr_unit_t> edge_builder;
        arrow::Int64Builder offset_builder;
        CHECK_ARROW_ERROR(offset_builder.Append(0));
        for (int offset = 0; offset < tvnums_[v_label]; ++offset) {
          for (int k = ie_offset[offset]; k < ie_offset[offset + 1]; ++k) {
            CHECK_ARROW_ERROR(
                edge_builder.Append(reinterpret_cast<const uint8_t*>(ie + k)));
          }
          for (int k = oe_offset[offset]; k < oe_offset[offset + 1]; ++k) {
            CHECK_ARROW_ERROR(
                edge_builder.Append(reinterpret_cast<const uint8_t*>(oe + k)));
          }
          CHECK_ARROW_ERROR(offset_builder.Append(edge_builder.length()));
        }
        CHECK_ARROW_ERROR(
            offset_builder.Finish(&oe_offsets_lists[v_label][e_label]));

        sort_edges_with_respect_to_vertex(edge_builder,
                                          oe_offsets_lists[v_label][e_label],
                                          tvnums_[v_label], concurrency);
        if (!is_multigraph) {
          check_is_multigraph(edge_builder, oe_offsets_lists[v_label][e_label],
                              tvnums_[v_label], concurrency, is_multigraph);
        }

        CHECK_ARROW_ERROR(edge_builder.Finish(&oe_lists[v_label][e_label]));
      }
    }
  }

  __attribute__((annotate("shared"))) fid_t fid_, fnum_;
  __attribute__((annotate("shared"))) bool directed_;
  __attribute__((annotate("shared"))) bool is_multigraph_;
  __attribute__((annotate("shared"))) property_graph_types::LABEL_ID_TYPE vertex_label_num_;
  __attribute__((annotate("shared"))) property_graph_types::LABEL_ID_TYPE edge_label_num_;
  size_t oenum_, ienum_;  // FIXME: should be pre-computable

  __attribute__((annotate("shared"))) String oid_type, vid_type;

  __attribute__((annotate("shared"))) vineyard::Array<vid_t> ivnums_, ovnums_, tvnums_;

  __attribute__((annotate("shared"))) List<std::shared_ptr<Table>> vertex_tables_;
  std::vector<std::vector<const void*>> vertex_tables_columns_;

  __attribute__((annotate("shared"))) List<std::shared_ptr<vid_vineyard_array_t>> ovgid_lists_;
  std::vector<const vid_t*> ovgid_lists_ptr_;

  __attribute__((annotate("shared"))) List<std::shared_ptr<vineyard::Hashmap<vid_t, vid_t>>> ovg2l_maps_;
  std::vector<vineyard::Hashmap<vid_t, vid_t>*> ovg2l_maps_ptr_;

  __attribute__((annotate("shared"))) List<std::shared_ptr<Table>> edge_tables_;
  std::vector<std::vector<const void*>> edge_tables_columns_;
  std::vector<const void**> flatten_edge_tables_columns_;

  __attribute__((annotate("shared"))) List<List<std::shared_ptr<FixedSizeBinaryArray>>> ie_lists_,
      oe_lists_;
  std::vector<std::vector<const nbr_unit_t*>> ie_ptr_lists_, oe_ptr_lists_;
  __attribute__((annotate("shared"))) List<List<std::shared_ptr<Int64Array>>> ie_offsets_lists_,
      oe_offsets_lists_;
  std::vector<std::vector<const int64_t*>> ie_offsets_ptr_lists_,
      oe_offsets_ptr_lists_;

  std::vector<std::vector<std::vector<fid_t>>> idst_, odst_, iodst_;
  std::vector<std::vector<std::vector<fid_t*>>> idoffset_, odoffset_,
      iodoffset_;

  __attribute__((annotate("shared"))) std::shared_ptr<vertex_map_t> vm_ptr_;

  vineyard::IdParser<vid_t> vid_parser_;

  __attribute__((annotate("shared"))) json schema_json_;
  PropertyGraphSchema schema_;

  friend class ArrowFragmentBaseBuilder<OID_T, VID_T>;

  template <typename _OID_T, typename _VID_T, typename VDATA_T,
            typename EDATA_T>
  friend class gs::ArrowProjectedFragment;
};

}  // namespace vineyard

#endif  // MODULES_GRAPH_FRAGMENT_ARROW_FRAGMENT_MOD_H_

namespace vineyard {

template<typename OID_T, typename VID_T>
class ArrowFragmentBaseBuilder: public ObjectBuilder {
  public:
    // using oid_t
    using oid_t = OID_T;
    // using vid_t
    using vid_t = VID_T;
    // using internal_oid_t
    using internal_oid_t = typename InternalType<oid_t>::type;
    // using eid_t
    using eid_t = property_graph_types::EID_TYPE;
    // using prop_id_t
    using prop_id_t = property_graph_types::PROP_ID_TYPE;
    // using label_id_t
    using label_id_t = property_graph_types::LABEL_ID_TYPE;
    // using vertex_range_t
    using vertex_range_t = grape::VertexRange<vid_t>;
    // using inner_vertices_t
    using inner_vertices_t = vertex_range_t;
    // using outer_vertices_t
    using outer_vertices_t = vertex_range_t;
    // using vertices_t
    using vertices_t = vertex_range_t;
    // using nbr_t
    using nbr_t = property_graph_utils::Nbr<vid_t, eid_t>;
    // using nbr_unit_t
    using nbr_unit_t = property_graph_utils::NbrUnit<vid_t, eid_t>;
    // using adj_list_t
    using adj_list_t = property_graph_utils::AdjList<vid_t, eid_t>;
    // using raw_adj_list_t
    using raw_adj_list_t = property_graph_utils::RawAdjList<vid_t, eid_t>;
    // using vertex_map_t
    using vertex_map_t = ArrowVertexMap<internal_oid_t, vid_t>;
    // using vertex_t
    using vertex_t = grape::Vertex<vid_t>;
    // using ovg2l_map_t
    using ovg2l_map_t =
      ska::flat_hash_map<vid_t, vid_t, typename Hashmap<vid_t, vid_t>::KeyHash>;
    // using vid_array_t
    using vid_array_t = typename vineyard::ConvertToArrowType<vid_t>::ArrayType;
    // using vid_vineyard_array_t
    using vid_vineyard_array_t =
      typename vineyard::ConvertToArrowType<vid_t>::VineyardArrayType;
    // using eid_array_t
    using eid_array_t = typename vineyard::ConvertToArrowType<eid_t>::ArrayType;
    // using eid_vineyard_array_t
    using eid_vineyard_array_t =
      typename vineyard::ConvertToArrowType<vid_t>::VineyardArrayType;
    // using vid_builder_t
    using vid_builder_t = typename ConvertToArrowType<vid_t>::BuilderType;

    explicit ArrowFragmentBaseBuilder(Client &client) {}

    explicit ArrowFragmentBaseBuilder(
            ArrowFragment<OID_T, VID_T> const &__value) {
        this->set_fid_(__value.fid_);
        this->set_fnum_(__value.fnum_);
        this->set_directed_(__value.directed_);
        this->set_is_multigraph_(__value.is_multigraph_);
        this->set_vertex_label_num_(__value.vertex_label_num_);
        this->set_edge_label_num_(__value.edge_label_num_);
        this->set_oid_type(__value.oid_type);
        this->set_vid_type(__value.vid_type);
        this->set_ivnums_(
            std::make_shared<typename std::decay<decltype(__value.ivnums_)>::type>(
                __value.ivnums_));
        this->set_ovnums_(
            std::make_shared<typename std::decay<decltype(__value.ovnums_)>::type>(
                __value.ovnums_));
        this->set_tvnums_(
            std::make_shared<typename std::decay<decltype(__value.tvnums_)>::type>(
                __value.tvnums_));
        for (auto const &__vertex_tables__item: __value.vertex_tables_) {
            this->add_vertex_tables_(__vertex_tables__item);
        }
        for (auto const &__ovgid_lists__item: __value.ovgid_lists_) {
            this->add_ovgid_lists_(__ovgid_lists__item);
        }
        for (auto const &__ovg2l_maps__item: __value.ovg2l_maps_) {
            this->add_ovg2l_maps_(__ovg2l_maps__item);
        }
        for (auto const &__edge_tables__item: __value.edge_tables_) {
            this->add_edge_tables_(__edge_tables__item);
        }
        this->ie_lists_.resize(__value.ie_lists_.size());
        for (size_t __idx = 0; __idx < __value.ie_lists_.size(); ++__idx) {
            this->ie_lists_[__idx].resize(__value.ie_lists_[__idx].size());
            for (size_t __idy = 0; __idy < __value.ie_lists_[__idx].size(); ++__idy) {
                this->ie_lists_[__idx][__idy] = __value.ie_lists_[__idx][__idy];
            }
        }
        this->oe_lists_.resize(__value.oe_lists_.size());
        for (size_t __idx = 0; __idx < __value.oe_lists_.size(); ++__idx) {
            this->oe_lists_[__idx].resize(__value.oe_lists_[__idx].size());
            for (size_t __idy = 0; __idy < __value.oe_lists_[__idx].size(); ++__idy) {
                this->oe_lists_[__idx][__idy] = __value.oe_lists_[__idx][__idy];
            }
        }
        this->ie_offsets_lists_.resize(__value.ie_offsets_lists_.size());
        for (size_t __idx = 0; __idx < __value.ie_offsets_lists_.size(); ++__idx) {
            this->ie_offsets_lists_[__idx].resize(__value.ie_offsets_lists_[__idx].size());
            for (size_t __idy = 0; __idy < __value.ie_offsets_lists_[__idx].size(); ++__idy) {
                this->ie_offsets_lists_[__idx][__idy] = __value.ie_offsets_lists_[__idx][__idy];
            }
        }
        this->oe_offsets_lists_.resize(__value.oe_offsets_lists_.size());
        for (size_t __idx = 0; __idx < __value.oe_offsets_lists_.size(); ++__idx) {
            this->oe_offsets_lists_[__idx].resize(__value.oe_offsets_lists_[__idx].size());
            for (size_t __idy = 0; __idy < __value.oe_offsets_lists_[__idx].size(); ++__idy) {
                this->oe_offsets_lists_[__idx][__idy] = __value.oe_offsets_lists_[__idx][__idy];
            }
        }
        this->set_vm_ptr_(__value.vm_ptr_);
        this->set_schema_json_(__value.schema_json_);
    }

    explicit ArrowFragmentBaseBuilder(
            std::shared_ptr<ArrowFragment<OID_T, VID_T>> const & __value):
        ArrowFragmentBaseBuilder(*__value) {
    }

    ObjectMeta &ValueMetaRef(std::shared_ptr<ArrowFragment<OID_T, VID_T>> &__value) {
        return __value->meta_;
    }

    std::shared_ptr<Object> _Seal(Client &client) override {
        // ensure the builder hasn't been sealed yet.
        ENSURE_NOT_SEALED(this);

        VINEYARD_CHECK_OK(this->Build(client));
        auto __value = std::make_shared<ArrowFragment<OID_T, VID_T>>();

        return this->_Seal(client, __value);
    }

    std::shared_ptr<Object> _Seal(Client &client, std::shared_ptr<ArrowFragment<OID_T, VID_T>> &__value) {
        size_t __value_nbytes = 0;

        __value->meta_.SetTypeName(type_name<ArrowFragment<OID_T, VID_T>>());
        if (std::is_base_of<GlobalObject, ArrowFragment<OID_T, VID_T>>::value) {
            __value->meta_.SetGlobal(true);
        }

        __value->fid_ = fid_;
        __value->meta_.AddKeyValue("fid_", __value->fid_);

        __value->fnum_ = fnum_;
        __value->meta_.AddKeyValue("fnum_", __value->fnum_);

        __value->directed_ = directed_;
        __value->meta_.AddKeyValue("directed_", __value->directed_);

        __value->is_multigraph_ = is_multigraph_;
        __value->meta_.AddKeyValue("is_multigraph_", __value->is_multigraph_);

        __value->vertex_label_num_ = vertex_label_num_;
        __value->meta_.AddKeyValue("vertex_label_num_", __value->vertex_label_num_);

        __value->edge_label_num_ = edge_label_num_;
        __value->meta_.AddKeyValue("edge_label_num_", __value->edge_label_num_);

        __value->oid_type = oid_type;
        __value->meta_.AddKeyValue("oid_type", __value->oid_type);

        __value->vid_type = vid_type;
        __value->meta_.AddKeyValue("vid_type", __value->vid_type);

        // using __ivnums__value_type = typename vineyard::Array<vid_t>;
        using __ivnums__value_type = decltype(__value->ivnums_);
        auto __value_ivnums_ = std::dynamic_pointer_cast<__ivnums__value_type>(
            ivnums_->_Seal(client));
        __value->ivnums_ = *__value_ivnums_;
        __value->meta_.AddMember("ivnums_", __value->ivnums_);
        __value_nbytes += __value_ivnums_->nbytes();

        // using __ovnums__value_type = typename vineyard::Array<vid_t>;
        using __ovnums__value_type = decltype(__value->ovnums_);
        auto __value_ovnums_ = std::dynamic_pointer_cast<__ovnums__value_type>(
            ovnums_->_Seal(client));
        __value->ovnums_ = *__value_ovnums_;
        __value->meta_.AddMember("ovnums_", __value->ovnums_);
        __value_nbytes += __value_ovnums_->nbytes();

        // using __tvnums__value_type = typename vineyard::Array<vid_t>;
        using __tvnums__value_type = decltype(__value->tvnums_);
        auto __value_tvnums_ = std::dynamic_pointer_cast<__tvnums__value_type>(
            tvnums_->_Seal(client));
        __value->tvnums_ = *__value_tvnums_;
        __value->meta_.AddMember("tvnums_", __value->tvnums_);
        __value_nbytes += __value_tvnums_->nbytes();

        // using __vertex_tables__value_type = typename List<std::shared_ptr<Table>>::value_type::element_type;
        using __vertex_tables__value_type = typename decltype(__value->vertex_tables_)::value_type::element_type;

        size_t __vertex_tables__idx = 0;
        for (auto &__vertex_tables__value: vertex_tables_) {
            auto __value_vertex_tables_ = std::dynamic_pointer_cast<__vertex_tables__value_type>(
                __vertex_tables__value->_Seal(client));
            __value->vertex_tables_.emplace_back(__value_vertex_tables_);
            __value->meta_.AddMember("__vertex_tables_-" + std::to_string(__vertex_tables__idx),
                                     __value_vertex_tables_);
            __value_nbytes += __value_vertex_tables_->nbytes();
            __vertex_tables__idx += 1;
        }
        __value->meta_.AddKeyValue("__vertex_tables_-size", __value->vertex_tables_.size());

        // using __ovgid_lists__value_type = typename List<std::shared_ptr<vid_vineyard_array_t>>::value_type::element_type;
        using __ovgid_lists__value_type = typename decltype(__value->ovgid_lists_)::value_type::element_type;

        size_t __ovgid_lists__idx = 0;
        for (auto &__ovgid_lists__value: ovgid_lists_) {
            auto __value_ovgid_lists_ = std::dynamic_pointer_cast<__ovgid_lists__value_type>(
                __ovgid_lists__value->_Seal(client));
            __value->ovgid_lists_.emplace_back(__value_ovgid_lists_);
            __value->meta_.AddMember("__ovgid_lists_-" + std::to_string(__ovgid_lists__idx),
                                     __value_ovgid_lists_);
            __value_nbytes += __value_ovgid_lists_->nbytes();
            __ovgid_lists__idx += 1;
        }
        __value->meta_.AddKeyValue("__ovgid_lists_-size", __value->ovgid_lists_.size());

        // using __ovg2l_maps__value_type = typename List<std::shared_ptr<vineyard::Hashmap<vid_t, vid_t>>>::value_type::element_type;
        using __ovg2l_maps__value_type = typename decltype(__value->ovg2l_maps_)::value_type::element_type;

        size_t __ovg2l_maps__idx = 0;
        for (auto &__ovg2l_maps__value: ovg2l_maps_) {
            auto __value_ovg2l_maps_ = std::dynamic_pointer_cast<__ovg2l_maps__value_type>(
                __ovg2l_maps__value->_Seal(client));
            __value->ovg2l_maps_.emplace_back(__value_ovg2l_maps_);
            __value->meta_.AddMember("__ovg2l_maps_-" + std::to_string(__ovg2l_maps__idx),
                                     __value_ovg2l_maps_);
            __value_nbytes += __value_ovg2l_maps_->nbytes();
            __ovg2l_maps__idx += 1;
        }
        __value->meta_.AddKeyValue("__ovg2l_maps_-size", __value->ovg2l_maps_.size());

        // using __edge_tables__value_type = typename List<std::shared_ptr<Table>>::value_type::element_type;
        using __edge_tables__value_type = typename decltype(__value->edge_tables_)::value_type::element_type;

        size_t __edge_tables__idx = 0;
        for (auto &__edge_tables__value: edge_tables_) {
            auto __value_edge_tables_ = std::dynamic_pointer_cast<__edge_tables__value_type>(
                __edge_tables__value->_Seal(client));
            __value->edge_tables_.emplace_back(__value_edge_tables_);
            __value->meta_.AddMember("__edge_tables_-" + std::to_string(__edge_tables__idx),
                                     __value_edge_tables_);
            __value_nbytes += __value_edge_tables_->nbytes();
            __edge_tables__idx += 1;
        }
        __value->meta_.AddKeyValue("__edge_tables_-size", __value->edge_tables_.size());

        // using __ie_lists__value_type = typename List<List<std::shared_ptr<FixedSizeBinaryArray>>>::value_type::value_type::element_type;
        using __ie_lists__value_type = typename decltype(__value->ie_lists_)::value_type::value_type::element_type;

        size_t __ie_lists__idx = 0;
        __value->ie_lists_.resize(ie_lists_.size());
        for (auto &__ie_lists__value_vec: ie_lists_) {
            size_t __ie_lists__idy = 0;
            __value->meta_.AddKeyValue("__ie_lists_-" + std::to_string(__ie_lists__idx) + "-size", __ie_lists__value_vec.size());
            for (auto &__ie_lists__value: __ie_lists__value_vec) {
                auto __value_ie_lists_ = std::dynamic_pointer_cast<__ie_lists__value_type>(
                    __ie_lists__value->_Seal(client));
                __value->ie_lists_[__ie_lists__idx].emplace_back(__value_ie_lists_);
                __value->meta_.AddMember("__ie_lists_-" + std::to_string(__ie_lists__idx) + "-" + std::to_string(__ie_lists__idy),
                                         __value_ie_lists_);
                __value_nbytes += __value_ie_lists_->nbytes();
                __ie_lists__idy += 1;
            }
            __ie_lists__idx += 1;
        }
        __value->meta_.AddKeyValue("__ie_lists_-size", __value->ie_lists_.size());

        // using __oe_lists__value_type = typename List<List<std::shared_ptr<FixedSizeBinaryArray>>>::value_type::value_type::element_type;
        using __oe_lists__value_type = typename decltype(__value->oe_lists_)::value_type::value_type::element_type;

        size_t __oe_lists__idx = 0;
        __value->oe_lists_.resize(oe_lists_.size());
        for (auto &__oe_lists__value_vec: oe_lists_) {
            size_t __oe_lists__idy = 0;
            __value->meta_.AddKeyValue("__oe_lists_-" + std::to_string(__oe_lists__idx) + "-size", __oe_lists__value_vec.size());
            for (auto &__oe_lists__value: __oe_lists__value_vec) {
                auto __value_oe_lists_ = std::dynamic_pointer_cast<__oe_lists__value_type>(
                    __oe_lists__value->_Seal(client));
                __value->oe_lists_[__oe_lists__idx].emplace_back(__value_oe_lists_);
                __value->meta_.AddMember("__oe_lists_-" + std::to_string(__oe_lists__idx) + "-" + std::to_string(__oe_lists__idy),
                                         __value_oe_lists_);
                __value_nbytes += __value_oe_lists_->nbytes();
                __oe_lists__idy += 1;
            }
            __oe_lists__idx += 1;
        }
        __value->meta_.AddKeyValue("__oe_lists_-size", __value->oe_lists_.size());

        // using __ie_offsets_lists__value_type = typename List<List<std::shared_ptr<Int64Array>>>::value_type::value_type::element_type;
        using __ie_offsets_lists__value_type = typename decltype(__value->ie_offsets_lists_)::value_type::value_type::element_type;

        size_t __ie_offsets_lists__idx = 0;
        __value->ie_offsets_lists_.resize(ie_offsets_lists_.size());
        for (auto &__ie_offsets_lists__value_vec: ie_offsets_lists_) {
            size_t __ie_offsets_lists__idy = 0;
            __value->meta_.AddKeyValue("__ie_offsets_lists_-" + std::to_string(__ie_offsets_lists__idx) + "-size", __ie_offsets_lists__value_vec.size());
            for (auto &__ie_offsets_lists__value: __ie_offsets_lists__value_vec) {
                auto __value_ie_offsets_lists_ = std::dynamic_pointer_cast<__ie_offsets_lists__value_type>(
                    __ie_offsets_lists__value->_Seal(client));
                __value->ie_offsets_lists_[__ie_offsets_lists__idx].emplace_back(__value_ie_offsets_lists_);
                __value->meta_.AddMember("__ie_offsets_lists_-" + std::to_string(__ie_offsets_lists__idx) + "-" + std::to_string(__ie_offsets_lists__idy),
                                         __value_ie_offsets_lists_);
                __value_nbytes += __value_ie_offsets_lists_->nbytes();
                __ie_offsets_lists__idy += 1;
            }
            __ie_offsets_lists__idx += 1;
        }
        __value->meta_.AddKeyValue("__ie_offsets_lists_-size", __value->ie_offsets_lists_.size());

        // using __oe_offsets_lists__value_type = typename List<List<std::shared_ptr<Int64Array>>>::value_type::value_type::element_type;
        using __oe_offsets_lists__value_type = typename decltype(__value->oe_offsets_lists_)::value_type::value_type::element_type;

        size_t __oe_offsets_lists__idx = 0;
        __value->oe_offsets_lists_.resize(oe_offsets_lists_.size());
        for (auto &__oe_offsets_lists__value_vec: oe_offsets_lists_) {
            size_t __oe_offsets_lists__idy = 0;
            __value->meta_.AddKeyValue("__oe_offsets_lists_-" + std::to_string(__oe_offsets_lists__idx) + "-size", __oe_offsets_lists__value_vec.size());
            for (auto &__oe_offsets_lists__value: __oe_offsets_lists__value_vec) {
                auto __value_oe_offsets_lists_ = std::dynamic_pointer_cast<__oe_offsets_lists__value_type>(
                    __oe_offsets_lists__value->_Seal(client));
                __value->oe_offsets_lists_[__oe_offsets_lists__idx].emplace_back(__value_oe_offsets_lists_);
                __value->meta_.AddMember("__oe_offsets_lists_-" + std::to_string(__oe_offsets_lists__idx) + "-" + std::to_string(__oe_offsets_lists__idy),
                                         __value_oe_offsets_lists_);
                __value_nbytes += __value_oe_offsets_lists_->nbytes();
                __oe_offsets_lists__idy += 1;
            }
            __oe_offsets_lists__idx += 1;
        }
        __value->meta_.AddKeyValue("__oe_offsets_lists_-size", __value->oe_offsets_lists_.size());

        // using __vm_ptr__value_type = typename std::shared_ptr<vertex_map_t>::element_type;
        using __vm_ptr__value_type = typename decltype(__value->vm_ptr_)::element_type;
        auto __value_vm_ptr_ = std::dynamic_pointer_cast<__vm_ptr__value_type>(
            vm_ptr_->_Seal(client));
        __value->vm_ptr_ = __value_vm_ptr_;
        __value->meta_.AddMember("vm_ptr_", __value->vm_ptr_);
        __value_nbytes += __value_vm_ptr_->nbytes();

        __value->schema_json_ = schema_json_;
        __value->meta_.AddKeyValue("schema_json_", __value->schema_json_);

        __value->meta_.SetNBytes(__value_nbytes);

        VINEYARD_CHECK_OK(client.CreateMetaData(__value->meta_, __value->id_));

        // mark the builder as sealed
        this->set_sealed(true);

        
        // run `PostConstruct` to return a valid object
        __value->PostConstruct(__value->meta_);

        return std::static_pointer_cast<Object>(__value);
    }

    Status Build(Client &client) override {
        return Status::OK();
    }

  protected:
    vineyard::fid_t fid_;
    vineyard::fid_t fnum_;
    bool directed_;
    bool is_multigraph_;
    property_graph_types::LABEL_ID_TYPE vertex_label_num_;
    property_graph_types::LABEL_ID_TYPE edge_label_num_;
    vineyard::String oid_type;
    vineyard::String vid_type;
    std::shared_ptr<ObjectBase> ivnums_;
    std::shared_ptr<ObjectBase> ovnums_;
    std::shared_ptr<ObjectBase> tvnums_;
    std::vector<std::shared_ptr<ObjectBase>> vertex_tables_;
    std::vector<std::shared_ptr<ObjectBase>> ovgid_lists_;
    std::vector<std::shared_ptr<ObjectBase>> ovg2l_maps_;
    std::vector<std::shared_ptr<ObjectBase>> edge_tables_;
    std::vector<std::vector<std::shared_ptr<ObjectBase>>> ie_lists_;
    std::vector<std::vector<std::shared_ptr<ObjectBase>>> oe_lists_;
    std::vector<std::vector<std::shared_ptr<ObjectBase>>> ie_offsets_lists_;
    std::vector<std::vector<std::shared_ptr<ObjectBase>>> oe_offsets_lists_;
    std::shared_ptr<ObjectBase> vm_ptr_;
    vineyard::json schema_json_;

    void set_fid_(vineyard::fid_t const &fid__) {
        this->fid_ = fid__;
    }

    void set_fnum_(vineyard::fid_t const &fnum__) {
        this->fnum_ = fnum__;
    }

    void set_directed_(bool const &directed__) {
        this->directed_ = directed__;
    }

    void set_is_multigraph_(bool const &is_multigraph__) {
        this->is_multigraph_ = is_multigraph__;
    }

    void set_vertex_label_num_(property_graph_types::LABEL_ID_TYPE const &vertex_label_num__) {
        this->vertex_label_num_ = vertex_label_num__;
    }

    void set_edge_label_num_(property_graph_types::LABEL_ID_TYPE const &edge_label_num__) {
        this->edge_label_num_ = edge_label_num__;
    }

    void set_oid_type(vineyard::String const &oid_type_) {
        this->oid_type = oid_type_;
    }

    void set_vid_type(vineyard::String const &vid_type_) {
        this->vid_type = vid_type_;
    }

    void set_ivnums_(std::shared_ptr<ObjectBase> const & ivnums__) {
        this->ivnums_ = ivnums__;
    }

    void set_ovnums_(std::shared_ptr<ObjectBase> const & ovnums__) {
        this->ovnums_ = ovnums__;
    }

    void set_tvnums_(std::shared_ptr<ObjectBase> const & tvnums__) {
        this->tvnums_ = tvnums__;
    }

    void set_vertex_tables_(std::vector<std::shared_ptr<ObjectBase>> const &vertex_tables__) {
        this->vertex_tables_ = vertex_tables__;
    }
    void set_vertex_tables_(size_t const idx, std::shared_ptr<ObjectBase> const &vertex_tables__) {
        if (idx >= this->vertex_tables_.size()) {
            this->vertex_tables_.resize(idx + 1);
        }
        this->vertex_tables_[idx] = vertex_tables__;
    }
    void add_vertex_tables_(std::shared_ptr<ObjectBase> const &vertex_tables__) {
        this->vertex_tables_.emplace_back(vertex_tables__);
    }

    void set_ovgid_lists_(std::vector<std::shared_ptr<ObjectBase>> const &ovgid_lists__) {
        this->ovgid_lists_ = ovgid_lists__;
    }
    void set_ovgid_lists_(size_t const idx, std::shared_ptr<ObjectBase> const &ovgid_lists__) {
        if (idx >= this->ovgid_lists_.size()) {
            this->ovgid_lists_.resize(idx + 1);
        }
        this->ovgid_lists_[idx] = ovgid_lists__;
    }
    void add_ovgid_lists_(std::shared_ptr<ObjectBase> const &ovgid_lists__) {
        this->ovgid_lists_.emplace_back(ovgid_lists__);
    }

    void set_ovg2l_maps_(std::vector<std::shared_ptr<ObjectBase>> const &ovg2l_maps__) {
        this->ovg2l_maps_ = ovg2l_maps__;
    }
    void set_ovg2l_maps_(size_t const idx, std::shared_ptr<ObjectBase> const &ovg2l_maps__) {
        if (idx >= this->ovg2l_maps_.size()) {
            this->ovg2l_maps_.resize(idx + 1);
        }
        this->ovg2l_maps_[idx] = ovg2l_maps__;
    }
    void add_ovg2l_maps_(std::shared_ptr<ObjectBase> const &ovg2l_maps__) {
        this->ovg2l_maps_.emplace_back(ovg2l_maps__);
    }

    void set_edge_tables_(std::vector<std::shared_ptr<ObjectBase>> const &edge_tables__) {
        this->edge_tables_ = edge_tables__;
    }
    void set_edge_tables_(size_t const idx, std::shared_ptr<ObjectBase> const &edge_tables__) {
        if (idx >= this->edge_tables_.size()) {
            this->edge_tables_.resize(idx + 1);
        }
        this->edge_tables_[idx] = edge_tables__;
    }
    void add_edge_tables_(std::shared_ptr<ObjectBase> const &edge_tables__) {
        this->edge_tables_.emplace_back(edge_tables__);
    }

    void set_ie_lists_(std::vector<std::vector<std::shared_ptr<ObjectBase>>> const &ie_lists__) {
        this->ie_lists_ = ie_lists__;
    }
    void set_ie_lists_(size_t const idx, std::vector<std::shared_ptr<ObjectBase>> const &ie_lists__) {
        if (idx >= this->ie_lists_.size()) {
            this->ie_lists_.resize(idx + 1);
        }
        this->ie_lists_[idx] = ie_lists__;
    }
    void set_ie_lists_(size_t const idx, size_t const idy,
                          std::shared_ptr<ObjectBase> const &ie_lists__) {
        if (idx >= this->ie_lists_.size()) {
            this->ie_lists_.resize(idx + 1);
        }
        if (idy >= this->ie_lists_[idx].size()) {
            this->ie_lists_[idx].resize(idy + 1);
        }
        this->ie_lists_[idx][idy] = ie_lists__;
    }
    void add_ie_lists_(std::vector<std::shared_ptr<ObjectBase>> const &ie_lists__) {
        this->ie_lists_.emplace_back(ie_lists__);
    }

    void set_oe_lists_(std::vector<std::vector<std::shared_ptr<ObjectBase>>> const &oe_lists__) {
        this->oe_lists_ = oe_lists__;
    }
    void set_oe_lists_(size_t const idx, std::vector<std::shared_ptr<ObjectBase>> const &oe_lists__) {
        if (idx >= this->oe_lists_.size()) {
            this->oe_lists_.resize(idx + 1);
        }
        this->oe_lists_[idx] = oe_lists__;
    }
    void set_oe_lists_(size_t const idx, size_t const idy,
                          std::shared_ptr<ObjectBase> const &oe_lists__) {
        if (idx >= this->oe_lists_.size()) {
            this->oe_lists_.resize(idx + 1);
        }
        if (idy >= this->oe_lists_[idx].size()) {
            this->oe_lists_[idx].resize(idy + 1);
        }
        this->oe_lists_[idx][idy] = oe_lists__;
    }
    void add_oe_lists_(std::vector<std::shared_ptr<ObjectBase>> const &oe_lists__) {
        this->oe_lists_.emplace_back(oe_lists__);
    }

    void set_ie_offsets_lists_(std::vector<std::vector<std::shared_ptr<ObjectBase>>> const &ie_offsets_lists__) {
        this->ie_offsets_lists_ = ie_offsets_lists__;
    }
    void set_ie_offsets_lists_(size_t const idx, std::vector<std::shared_ptr<ObjectBase>> const &ie_offsets_lists__) {
        if (idx >= this->ie_offsets_lists_.size()) {
            this->ie_offsets_lists_.resize(idx + 1);
        }
        this->ie_offsets_lists_[idx] = ie_offsets_lists__;
    }
    void set_ie_offsets_lists_(size_t const idx, size_t const idy,
                          std::shared_ptr<ObjectBase> const &ie_offsets_lists__) {
        if (idx >= this->ie_offsets_lists_.size()) {
            this->ie_offsets_lists_.resize(idx + 1);
        }
        if (idy >= this->ie_offsets_lists_[idx].size()) {
            this->ie_offsets_lists_[idx].resize(idy + 1);
        }
        this->ie_offsets_lists_[idx][idy] = ie_offsets_lists__;
    }
    void add_ie_offsets_lists_(std::vector<std::shared_ptr<ObjectBase>> const &ie_offsets_lists__) {
        this->ie_offsets_lists_.emplace_back(ie_offsets_lists__);
    }

    void set_oe_offsets_lists_(std::vector<std::vector<std::shared_ptr<ObjectBase>>> const &oe_offsets_lists__) {
        this->oe_offsets_lists_ = oe_offsets_lists__;
    }
    void set_oe_offsets_lists_(size_t const idx, std::vector<std::shared_ptr<ObjectBase>> const &oe_offsets_lists__) {
        if (idx >= this->oe_offsets_lists_.size()) {
            this->oe_offsets_lists_.resize(idx + 1);
        }
        this->oe_offsets_lists_[idx] = oe_offsets_lists__;
    }
    void set_oe_offsets_lists_(size_t const idx, size_t const idy,
                          std::shared_ptr<ObjectBase> const &oe_offsets_lists__) {
        if (idx >= this->oe_offsets_lists_.size()) {
            this->oe_offsets_lists_.resize(idx + 1);
        }
        if (idy >= this->oe_offsets_lists_[idx].size()) {
            this->oe_offsets_lists_[idx].resize(idy + 1);
        }
        this->oe_offsets_lists_[idx][idy] = oe_offsets_lists__;
    }
    void add_oe_offsets_lists_(std::vector<std::shared_ptr<ObjectBase>> const &oe_offsets_lists__) {
        this->oe_offsets_lists_.emplace_back(oe_offsets_lists__);
    }

    void set_vm_ptr_(std::shared_ptr<ObjectBase> const & vm_ptr__) {
        this->vm_ptr_ = vm_ptr__;
    }

    void set_schema_json_(vineyard::json const &schema_json__) {
        this->schema_json_ = schema_json__;
    }

  private:
    friend class ArrowFragment<OID_T, VID_T>;
};


}  // namespace vineyard



#endif // MODULES_GRAPH_FRAGMENT_ARROW_FRAGMENT_VINEYARD_H
