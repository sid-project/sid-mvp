/*
 * This file is part of SID.
 *
 * Copyright (C) 2017-2018 Red Hat, Inc. All rights reserved.
 *
 * SID is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 2 of the License, or
 * (at your option) any later version.
 *
 * SID is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with SID.  If not, see <http://www.gnu.org/licenses/>.
*/

#ifndef _SID_KV_STORE_H
#define _SID_KV_STORE_H

#include "resource.h"

#include <sys/uio.h>

#ifdef __cplusplus
extern "C" {
#endif

#define KV_STORE_KEY_JOIN ":"

typedef enum {
	KV_STORE_BACKEND_HASH,
} kv_store_backend_t;

#define KV_STORE_VALUE_VECTOR    UINT32_C(0x00000001)
#define KV_STORE_VALUE_REF       UINT32_C(0x00000002)
#define KV_STORE_VALUE_AUTOFREE  UINT32_C(0x00000004)

#define KV_STORE_VALUE_OP_MERGE  UINT32_C(0x00000001)

struct kv_store_hash_backend_params {
	size_t initial_size;
};

struct sid_kv_store_resource_params {
	kv_store_backend_t backend;
	union {
		struct kv_store_hash_backend_params hash;
	};
};

/*
 * Returns:
 *   0 to keep old_data
 *   1 to update old_data with new_data
 */
typedef int (*kv_store_update_fn_t) (const char *key_prefix, const char *key,
				     void *old_value, size_t old_value_size,
				     void **new_value, size_t *new_value_size,
				     void *arg);

/*
 * Sets key-value pair:
 *   - Final key is composed of key_prefix and key.
 *   - kv_update_fn callback with kv_update_fn_arg is called before updating the value.
 *   - Value and size depend on flags with KV_STORE_VALUE_ prefix, see table below.
 *     INPUT VALUE:  value as provided via kv_store_set_value's "value" argument.
 *     INPUT SIZE:   value size as provided via kv_store_set_value's "value_size" argument.
 *     OUTPUT VALUE: value as returned by kv_store_{set,get}_value.
 *     OUTPUT SIZE:  value size as returned by kv_store_get_value.
 *
 *  - Flag support depends on used backend.
 *
 *       FLAG     OP_FLAG         INPUT                        OUTPUT
 *         |         |              |                            |
 *     ---------    ---    ---------------------    -------------------------------
 *    /         \  /   \  /                     \  /                               \
 * #  VECTOR  REF  MERGE  INPUT_VALUE  INPUT_SIZE  OUTPUT_VALUE           OUTPUT_SIZE  NOTE
 * ---------------------------------------------------------------------------------------------------------------------------------------------------------------
 * A    0      0     0    value ref    value size  value copy ref         value size
 * B    0      0     1    value ref    value size  value copy ref         value size   merge flag has no effect: B == A
 * C    0      1     0    value ref    value size  value ref              value size
 * D    0      1     1    value ref    value size  value ref              value size   merge flag has no effect: D == C
 * E    1      0     0    iovec ref    iovec size  iovec deep copy ref    iovec size
 * F    1      0     1    iovec ref    iovec size  value merger ref       value size   iovec members merged into single value
 * G    1      1     0    iovec ref    iovec size  iovec ref              iovec size
 * H    1      1     1    iovec ref    iovec size  value merger iovec ref iovec size   iovec members merged into single value, iovec has refs to merged value parts
 *
 * Returns:
 *   The value that has been set.
 */
void *kv_store_set_value(sid_resource_t *kv_store_res, const char *key_prefix, const char *key,
			 void *value, size_t value_size, uint32_t flags, uint64_t op_flags,
			 kv_store_update_fn_t kv_update_fn, void *kv_update_fn_arg);
/*
 * Gets value for given key.
 *   - Final key is composed of key_prefix and key.
 *   - If value_size is not NULL, the function returns the size of the value through this output argument.
 */
void *kv_store_get_value(sid_resource_t *kv_store_res, const char *key_prefix, const char *key, size_t *value_size);

/*
 * Unsets value for given key.
 *   - Final key is composed of key_prefix and key.
 *   - Before the value is actually unset, unset_resolver with unset_resolver_arg is called to confirm the action.
 *
 * Returns:
 *    0 if value unset
 *   -1 if value not unset
 */
int kv_store_unset_value(sid_resource_t *kv_store_res, const char *key_prefix, const char *key,
			 kv_store_update_fn_t kv_unset_fn, void *kv_unset_fn_arg);

typedef struct kv_store_iter kv_store_iter_t;

kv_store_iter_t *kv_store_iter_create(sid_resource_t *kv_store_res);
const char *kv_store_iter_current_key(kv_store_iter_t *iter);
void *kv_store_iter_current(kv_store_iter_t *iter, size_t *size, uint32_t *flags);
void *kv_store_iter_next(kv_store_iter_t *iter, size_t *size, uint32_t *flags);
void kv_store_iter_reset(kv_store_iter_t *iter);
void kv_store_iter_destroy(kv_store_iter_t *iter);

#ifdef __cplusplus
}
#endif

#endif
