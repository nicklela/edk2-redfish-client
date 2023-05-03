//
// Auto-generated file by Redfish Schema C Structure Generator.
// https://github.com/DMTF/Redfish-Schema-C-Struct-Generator.
//
//  (C) Copyright 2019-2021 Hewlett Packard Enterprise Development LP<BR>
//
// Copyright Notice:
// Copyright 2019-2021 Distributed Management Task Force, Inc. All rights reserved.
// License: BSD 3-Clause License. For full text see link: https://github.com/DMTF/Redfish-JSON-C-Struct-Converter/blob/master/LICENSE.md
//

#ifndef RedfishUpdateservice_V1_0_7_CSTRUCT_H_
#define RedfishUpdateservice_V1_0_7_CSTRUCT_H_

#include "RedfishCsCommon.h"

#ifndef RedfishResource_Condition_CS_
#ifndef RedfishResource_Condition_Array_CS_
typedef struct _RedfishResource_Condition_Array_CS RedfishResource_Condition_Array_CS;
#endif
typedef struct _RedfishResource_Condition_CS RedfishResource_Condition_CS;
#endif

#ifndef RedfishResource_Oem_CS_
typedef struct _RedfishResource_Oem_CS RedfishResource_Oem_CS;
#endif

#ifndef RedfishResource_Status_CS_
typedef struct _RedfishResource_Status_CS RedfishResource_Status_CS;
#endif

typedef struct _RedfishUpdateService_V1_0_7_Actions_CS RedfishUpdateService_V1_0_7_Actions_CS;
typedef struct _RedfishUpdateService_V1_0_7_OemActions_CS RedfishUpdateService_V1_0_7_OemActions_CS;
typedef struct _RedfishUpdateService_V1_0_7_SimpleUpdate_CS RedfishUpdateService_V1_0_7_SimpleUpdate_CS;
typedef struct _RedfishUpdateService_V1_0_7_UpdateService_CS RedfishUpdateService_V1_0_7_UpdateService_CS;
#ifndef Redfishodatav4_idRef_CS_
typedef struct _Redfishodatav4_idRef_CS Redfishodatav4_idRef_CS;
#endif

//
// A condition that requires attention.
//
#ifndef RedfishResource_Condition_CS_
#define RedfishResource_Condition_CS_
typedef struct _RedfishResource_Condition_CS {
    RedfishCS_Link             LogEntry;             // The link to the log entry
                                                     // created for this condition.
    RedfishCS_char             *Message;             // The human-readable message for
                                                     // this condition.
    RedfishCS_char_Array       *MessageArgs;         // An array of message arguments
                                                     // that are substituted for the
                                                     // arguments in the message when
                                                     // looked up in the message
                                                     // registry.
    RedfishCS_char             *MessageId;           // The identifier for the
                                                     // message.
    Redfishodatav4_idRef_CS    *OriginOfCondition;    // A link to the resource or
                                                     // object that originated the
                                                     // condition.
    RedfishCS_char             *Severity;            // The severity of the condition.
    RedfishCS_char             *Timestamp;           // The time the condition
                                                     // occurred.
} RedfishResource_Condition_CS;
#endif

//
// The OEM extension.
//
#ifndef RedfishResource_Oem_CS_
#define RedfishResource_Oem_CS_
typedef struct _RedfishResource_Oem_CS {
    RedfishCS_Link    Prop;
} RedfishResource_Oem_CS;
#endif

//
// The status and health of a resource and its children.
//
#ifndef RedfishResource_Status_CS_
#define RedfishResource_Status_CS_
typedef struct _RedfishResource_Status_CS {
    RedfishResource_Condition_Array_CS    *Conditions;     // Conditions in this resource
                                                           // that require attention.
    RedfishCS_char                        *Health;         // The health state of this
                                                           // resource in the absence of its
                                                           // dependent resources.
    RedfishCS_char                        *HealthRollup;    // The overall health state from
                                                           // the view of this resource.
    RedfishResource_Oem_CS                *Oem;            // The OEM extension property.
    RedfishCS_char                        *State;          // The known state of the
                                                           // resource, such as, enabled.
} RedfishResource_Status_CS;
#endif

//
// The available actions for this Resource.
//
typedef struct _RedfishUpdateService_V1_0_7_Actions_CS {
    RedfishUpdateService_V1_0_7_SimpleUpdate_CS    *UpdateService_SimpleUpdate;
    RedfishUpdateService_V1_0_7_OemActions_CS      *Oem;                          // The available OEM-specific
                                                                                  // actions for this Resource.
} RedfishUpdateService_V1_0_7_Actions_CS;

//
// The available OEM-specific actions for this Resource.
//
typedef struct _RedfishUpdateService_V1_0_7_OemActions_CS {
    RedfishCS_Link    Prop;
} RedfishUpdateService_V1_0_7_OemActions_CS;

//
// This action updates software components.
//
typedef struct _RedfishUpdateService_V1_0_7_SimpleUpdate_CS {
    RedfishCS_char    *target;    // Link to invoke action
    RedfishCS_char    *title;    // Friendly action name
} RedfishUpdateService_V1_0_7_SimpleUpdate_CS;

//
// A reference to a resource.
//
#ifndef Redfishodatav4_idRef_CS_
#define Redfishodatav4_idRef_CS_
typedef struct _Redfishodatav4_idRef_CS {
    RedfishCS_char    *odata_id;
} Redfishodatav4_idRef_CS;
#endif

//
// The UpdateService schema describes the Update Service and the properties for
// the Service itself with links to collections of firmware and software
// inventory.  The Update Service also provides methods for updating software and
// firmware of the Resources in a Redfish Service.
//
typedef struct _RedfishUpdateService_V1_0_7_UpdateService_CS {
    RedfishCS_Header                          Header;
    RedfishCS_char                            *odata_context;  
    RedfishCS_char                            *odata_etag;     
    RedfishCS_char                            *odata_id;       
    RedfishCS_char                            *odata_type;     
    RedfishUpdateService_V1_0_7_Actions_CS    *Actions;            // The available actions for this
                                                                   // Resource.
    RedfishCS_char                            *Description;    
    RedfishCS_Link                            FirmwareInventory;    // An inventory of firmware.
    RedfishCS_char                            *Id;             
    RedfishCS_char                            *Name;           
    RedfishResource_Oem_CS                    *Oem;                // The OEM extension property.
    RedfishCS_bool                            *ServiceEnabled;     // An indication of whether this
                                                                   // service is enabled.
    RedfishCS_Link                            SoftwareInventory;    // An inventory of software.
    RedfishResource_Status_CS                 *Status;             // The status and health of the
                                                                   // Resource and its subordinate
                                                                   // or dependent Resources.
} RedfishUpdateService_V1_0_7_UpdateService_CS;

#ifndef RedfishResource_Condition_Array_CS_
#define RedfishResource_Condition_Array_CS_
typedef struct _RedfishResource_Condition_Array_CS  {
    RedfishResource_Condition_Array_CS    *Next;
    RedfishResource_Condition_CS    *ArrayValue;
} RedfishResource_Condition_Array_CS;
#endif

RedfishCS_status
Json_UpdateService_V1_0_7_To_CS (char *JsonRawText, RedfishUpdateService_V1_0_7_UpdateService_CS **ReturnedCS);

RedfishCS_status
CS_To_UpdateService_V1_0_7_JSON (RedfishUpdateService_V1_0_7_UpdateService_CS *CSPtr, char **JsonText);

RedfishCS_status
DestroyUpdateService_V1_0_7_CS (RedfishUpdateService_V1_0_7_UpdateService_CS *CSPtr);

RedfishCS_status
DestroyUpdateService_V1_0_7_Json (RedfishCS_char *JsonText);

#endif
