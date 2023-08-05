// Protocol Buffers - Google's data interchange format
// Copyright 2008 Google Inc.  All rights reserved.
// https://developers.google.com/protocol-buffers/
//
// Redistribution and use in source and binary forms, with or without
// modification, are permitted provided that the following conditions are
// met:
//
//     * Redistributions of source code must retain the above copyright
// notice, this list of conditions and the following disclaimer.
//     * Redistributions in binary form must reproduce the above
// copyright notice, this list of conditions and the following disclaimer
// in the documentation and/or other materials provided with the
// distribution.
//     * Neither the name of Google Inc. nor the names of its
// contributors may be used to endorse or promote products derived from
// this software without specific prior written permission.
//
// THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
// "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
// LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
// A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
// OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
// SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
// LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
// DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
// THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
// (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
// OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

// This file contains declarations needed in generated headers for messages
// that use tail-call table parsing. Everything in this file is for internal
// use only.

#ifndef GOOGLE_PROTOBUF_GENERATED_MESSAGE_TCTABLE_DECL_H__
#define GOOGLE_PROTOBUF_GENERATED_MESSAGE_TCTABLE_DECL_H__

#include <cstdint>
#include <type_traits>

#include <google/protobuf/parse_context.h>
#include <google/protobuf/message_lite.h>

namespace google {
namespace protobuf {
namespace internal {

// Additional information about this field:
struct TcFieldData {
  constexpr TcFieldData() : data(0) {}
  constexpr TcFieldData(uint16_t coded_tag, uint8_t hasbit_idx, uint16_t offset)
      : data(static_cast<uint64_t>(offset) << 48 |
             static_cast<uint64_t>(hasbit_idx) << 16 | coded_tag) {}

  uint16_t coded_tag() const { return static_cast<uint16_t>(data); }
  uint8_t hasbit_idx() const { return static_cast<uint8_t>(data >> 16); }
  uint16_t offset() const { return static_cast<uint16_t>(data >> 48); }

  uint64_t data;
};

struct TailCallParseTableBase;

// TailCallParseFunc is the function pointer type used in the tailcall table.
typedef const char* (*TailCallParseFunc)(MessageLite* msg, const char* ptr,
                                         ParseContext* ctx,
                                         const TailCallParseTableBase* table,
                                         uint64_t hasbits, TcFieldData data);

// Base class for message-level table with info for the tail-call parser.
struct TailCallParseTableBase {
  // Common attributes for message layout:
  uint16_t has_bits_offset;
  uint16_t extension_offset;
  uint32_t extension_range_low;
  uint32_t extension_range_high;
  uint32_t has_bits_required_mask;
  const MessageLite* default_instance;

  // Handler for fields which are not handled by table dispatch.
  TailCallParseFunc fallback;

  // Table entry for fast-path tailcall dispatch handling.
  struct FieldEntry {
    // Target function for dispatch:
    TailCallParseFunc target;
    // Field data used during parse:
    TcFieldData bits;
  };
  // There is always at least one table entry.
  const FieldEntry* table() const {
    return reinterpret_cast<const FieldEntry*>(this + 1);
  }
};

static_assert(sizeof(TailCallParseTableBase::FieldEntry) <= 16,
              "Field entry is too big.");

template <size_t kTableSizeLog2>
struct TailCallParseTable {
  TailCallParseTableBase header;

  // Entries for each field.
  //
  // Fields are indexed by the lowest bits of their field number. The field
  // number is masked to fit inside the table. Note that the parsing logic
  // generally calls `TailCallParseTableBase::table()` instead of accessing
  // this field directly.
  TailCallParseTableBase::FieldEntry entries[(1 << kTableSizeLog2)];
};

static_assert(std::is_standard_layout<TailCallParseTable<1>>::value,
              "TailCallParseTable must be standard layout.");

static_assert(offsetof(TailCallParseTable<1>, entries) ==
                  sizeof(TailCallParseTableBase),
              "Table entries must be laid out after TailCallParseTableBase.");

}  // namespace internal
}  // namespace protobuf
}  // namespace google

#endif  // GOOGLE_PROTOBUF_GENERATED_MESSAGE_TCTABLE_DECL_H__
