/*
 * This file is part of SID.
 *
 * Copyright (C) 2019 Red Hat, Inc. All rights reserved.
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

#ifndef _SID_USID_IFACE_H
#define _SID_USID_IFACE_H

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>

#ifdef __cplusplus
extern "C" {
#endif

#define USID_PROTOCOL 2

typedef enum
{
	_USID_CMD_START     = 0,
	USID_CMD_UNDEFINED  = _USID_CMD_START, /* virtual cmd if cmd not defined at all */
	USID_CMD_UNKNOWN    = 1,               /* virtual cmd if cmd defined, but not recognized */
	USID_CMD_ACTIVE     = 2,
	USID_CMD_CHECKPOINT = 3,
	USID_CMD_REPLY      = 4,
	USID_CMD_SCAN       = 5,
	USID_CMD_VERSION    = 6,
	USID_CMD_DUMP       = 7,
	USID_CMD_STATS      = 8,
	USID_CMD_TREE       = 9,
	_USID_CMD_END       = USID_CMD_TREE,
} usid_cmd_t;

static const char *const usid_cmd_names[] = {
	[USID_CMD_UNDEFINED]  = "undefined",
	[USID_CMD_UNKNOWN]    = "unknown",
	[USID_CMD_ACTIVE]     = "active",
	[USID_CMD_CHECKPOINT] = "checkpoint",
	[USID_CMD_REPLY]      = "reply",
	[USID_CMD_SCAN]       = "scan",
	[USID_CMD_VERSION]    = "version",
	[USID_CMD_DUMP]       = "dump",
	[USID_CMD_STATS]      = "stats",
	[USID_CMD_TREE]       = "tree",
};

#define USID_CMD_STATUS_MASK_OVERALL UINT64_C(0x0000000000000001)
#define USID_CMD_STATUS_SUCCESS      UINT64_C(0x0000000000000000)
#define USID_CMD_STATUS_FAILURE      UINT64_C(0x0000000000000001)

#define USID_CMD_FLAGS_FMT_MASK        UINT16_C(0x0003)
#define USID_CMD_FLAGS_FMT_TABLE       UINT16_C(0x0000)
#define USID_CMD_FLAGS_FMT_JSON        UINT16_C(0x0001)
#define USID_CMD_FLAGS_FMT_ENV         UINT16_C(0x0002)
#define USID_CMD_FLAGS_UNMODIFIED_DATA UINT16_C(0x0004)

struct usid_checkpoint_data {
	char *       name;
	char **      keys;
	unsigned int nr_keys;
};

struct usid_unmodified_data {
	char * mem;
	size_t size;
};

struct usid_request {
	usid_cmd_t cmd;
	uint64_t   flags;
	uint64_t   seqnum;
	union {
		struct usid_checkpoint_data checkpoint;
		struct usid_unmodified_data unmodified;
	} data;
};

struct usid_result;

usid_cmd_t  usid_cmd_name_to_type(const char *cmd_name);
int         usid_req(struct usid_request *req, struct usid_result **res);
void        usid_result_free(struct usid_result *res);
int         usid_result_status(struct usid_result *res, uint64_t *status);
int         usid_result_protocol(struct usid_result *res, uint8_t *prot);
const char *usid_result_data(struct usid_result *res, size_t *size_p);
#ifdef __cplusplus
}
#endif

#endif