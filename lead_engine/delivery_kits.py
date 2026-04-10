from __future__ import annotations

from copy import deepcopy

PRELAUNCH_MODE = True

OFFER_TYPES = {
    "public": "Public",
    "internal": "Internal",
}

BUILD_STATUSES = {
    "planned": "Planned",
    "hardening": "Hardening",
    "verification": "Verification",
    "ready": "Ready",
}

BUILD_STATUS_ORDER = {
    "planned": 0,
    "hardening": 1,
    "verification": 2,
    "ready": 3,
}

VISIBILITY_STATES = {
    "hidden": "Hidden",
    "internal": "Internal",
    "ready": "Ready",
}

ACTIVATION_PACKET_SECTIONS = [
    "Client identity",
    "Sold scope",
    "Required access",
    "Required assets",
    "Decision approvals",
    "Execution settings",
    "Handoff checklist",
]

GLOBAL_POLICIES = {
    "revision_policy": "One standard revision window inside the sold fixed-price scope. New deliverables, channels, platforms, or deployment footprint changes become a change order.",
    "access_policy": "Track access state in Copperline, never in repo-tracked files. Use client-owned delegated access by default and confirm long-term ownership at closeout.",
    "support_policy": "Support is optional unless a managed automation module explicitly requires ongoing oversight.",
    "rollback_policy": "Messaging and automation modules must support a safe pause or disable path before launch.",
}


DELIVERY_CATALOG = {
    "presence_refresh": {
        "label": "Presence Refresh",
        "type": "core_offer",
        "offer_type": "public",
        "build_status": "hardening",
        "launch_eligible": False,
        "target_build_status": "ready",
        "kit_key": "presence_refresh_v1",
        "kit_version": "v1",
        "current_truth_note": "Real kit files now exist: asset request template, access checklist, cleanup checklist, QA checklist, and closeout snapshot template. Not yet proven in a live delivery.",
        "target_truth_note": "Ready once the kit has been used for one real client delivery and all checklist items are verified as repeatable.",
        "summary": "A bounded presence cleanup covering GBP, Facebook/basic social consistency, trust copy, and contact accuracy.",
        "includes": [
            "Google Business Profile refresh",
            "Facebook/basic presence refresh",
            "Hours, contact, and service consistency",
            "Trust-copy and photo cleanup",
        ],
        "required_artifacts": [
            "Logo or brand reference",
            "Current hours and service area",
            "Service list",
            "Business photos",
        ],
        "access_requirements": [
            "Google Business Profile access",
            "Facebook page access if used",
        ],
        "qa_checks": [
            "Profile details updated",
            "Contact info matches everywhere",
            "Photos and trust copy reviewed",
            "Presence QA checklist passed",
            "Before/after snapshot stored",
        ],
        "definition_of_done": [
            "Assets received from client",
            "Access confirmed on all in-scope platforms",
            "Profiles audited and updated",
            "Contact info consistent across platforms",
            "Photos and copy refreshed",
            "QA checklist passed",
            "Closeout snapshot stored",
        ],
        "missing_artifacts": [],
        "missing_qa": [],
        "missing_closeout": [],
        "missing_rollback": [],
        "artifact_files": {
            "asset_request_template": "lead_engine/delivery_kits/presence_refresh/asset_request_template.md",
            "access_checklist": "lead_engine/delivery_kits/presence_refresh/access_checklist.md",
            "presence_cleanup_checklist": "lead_engine/delivery_kits/presence_refresh/presence_cleanup_checklist.md",
            "presence_qa_checklist": "lead_engine/delivery_kits/presence_refresh/presence_qa_checklist.md",
            "closeout_snapshot_template": "lead_engine/delivery_kits/presence_refresh/closeout_snapshot_template.md",
        },
        "promotion_criteria": [
            "Kit used on at least one real client delivery",
            "All checklist items completed without gaps",
            "Closeout snapshot on file for the delivery",
            "No open issues in the QA log",
        ],
        "next_hardening_step": "Use the kit on a real Presence Refresh delivery. Track any checklist gaps or missing steps. Promote to verification once one delivery is cleanly closed out.",
        "ownership_mode": "client_owned",
        "support_policy_key": "optional_support",
        "support_summary": "Can be delivered as one-time work with optional monthly support.",
        "rollback_plan": [],
    },
    "starter_website": {
        "label": "Starter Website",
        "type": "core_offer",
        "offer_type": "public",
        "build_status": "hardening",
        "launch_eligible": False,
        "target_build_status": "ready",
        "kit_key": "starter_website_v1",
        "kit_version": "v1",
        "current_truth_note": "Real kit files now exist: content intake form, asset checklist, domain/hosting decision worksheet, publish checklist, and handoff closeout. Not yet proven in a live delivery.",
        "target_truth_note": "Ready once the kit has been used for one real client delivery, site published and live, and closeout confirmed.",
        "summary": "A one-page static site with a service summary, trust section, and clear contact CTA.",
        "includes": [
            "One-page static site",
            "Hero, services, trust, and CTA sections",
            "Mobile-friendly layout",
            "Contact CTA wired",
        ],
        "required_artifacts": [
            "Logo or wordmark",
            "Service list",
            "Business summary",
            "Photos",
            "Primary CTA/contact details",
        ],
        "access_requirements": [
            "Domain or hosting access",
            "Contact destination details",
        ],
        "qa_checks": [
            "Content review complete — no placeholder text",
            "All links working",
            "Mobile layout correct",
            "Contact CTA tested end-to-end",
            "DNS and HTTPS confirmed",
            "Site loads at correct URL",
            "Owner can access on phone",
        ],
        "definition_of_done": [
            "Content intake form completed with owner",
            "All required assets collected",
            "Domain and hosting decisions confirmed",
            "One-page site built to approved content",
            "Mobile QA passed",
            "Contact CTA tested and working",
            "Publish checklist completed",
            "Site live at correct URL",
            "Handoff closeout issued",
        ],
        "missing_artifacts": [],
        "missing_qa": [],
        "missing_closeout": [],
        "missing_rollback": [],
        "artifact_files": {
            "content_intake_form": "lead_engine/delivery_kits/starter_website/content_intake_form.md",
            "asset_checklist": "lead_engine/delivery_kits/starter_website/asset_checklist.md",
            "domain_hosting_decision": "lead_engine/delivery_kits/starter_website/domain_hosting_decision.md",
            "publish_checklist": "lead_engine/delivery_kits/starter_website/publish_checklist.md",
            "handoff_closeout": "lead_engine/delivery_kits/starter_website/handoff_closeout.md",
        },
        "promotion_criteria": [
            "Kit used on at least one real client delivery",
            "Site published and live at client URL",
            "Contact CTA tested and working",
            "Publish checklist completed and on file",
            "Handoff closeout issued and owner acknowledged",
        ],
        "next_hardening_step": "Use the kit on a real Starter Website delivery. Complete the publish checklist. Promote to verification once one site is live and cleanly handed off.",
        "ownership_mode": "hybrid",
        "support_policy_key": "optional_support",
        "support_summary": "Delivered as fixed project work with optional support for edits and upkeep.",
        "rollback_plan": [],
    },
    "lead_contact_setup": {
        "label": "Lead & Contact Setup",
        "type": "core_offer",
        "offer_type": "public",
        "build_status": "hardening",
        "launch_eligible": False,
        "target_build_status": "ready",
        "kit_key": "lead_contact_setup_v1",
        "kit_version": "v1",
        "current_truth_note": "Real kit files now exist: intake/routing worksheet, access checklist, notification preference template, routing test script, and handoff closeout. Not yet proven in a live delivery.",
        "target_truth_note": "Ready once the kit has been used for one real client delivery, all test script channels passed, and closeout was cleanly issued.",
        "summary": "A standard intake and contact-routing package for inquiries, callbacks, and follow-through.",
        "includes": [
            "Intake flow mapping",
            "Routing and owner notification rules",
            "Follow-up timing setup",
            "Basic test-and-handoff",
        ],
        "required_artifacts": [
            "Preferred contact destinations",
            "Notification preferences",
            "Service categories or intake paths",
        ],
        "access_requirements": [
            "Phone, email, or contact form routing access",
            "Any messaging tool access being used",
        ],
        "qa_checks": [
            "Intake map defined and scope bounded",
            "Access confirmed before setup begins",
            "Routing tested on all active channels",
            "Owner notification verified",
            "Follow-up path confirmed",
            "All routing test script channels passed",
        ],
        "definition_of_done": [
            "Intake / routing worksheet completed and owner-reviewed",
            "Access confirmed on all active channels",
            "Notification preferences captured and approved",
            "All active routing paths tested and passed",
            "Owner notification verified",
            "Handoff closeout issued to owner",
        ],
        "missing_artifacts": [],
        "missing_qa": [],
        "missing_closeout": [],
        "missing_rollback": [],
        "artifact_files": {
            "intake_routing_worksheet": "lead_engine/delivery_kits/lead_contact_setup/intake_routing_worksheet.md",
            "access_checklist": "lead_engine/delivery_kits/lead_contact_setup/access_checklist.md",
            "notification_preference_template": "lead_engine/delivery_kits/lead_contact_setup/notification_preference_template.md",
            "routing_test_script": "lead_engine/delivery_kits/lead_contact_setup/routing_test_script.md",
            "handoff_closeout": "lead_engine/delivery_kits/lead_contact_setup/handoff_closeout.md",
        },
        "promotion_criteria": [
            "Kit used on at least one real client delivery",
            "All routing test script channels passed",
            "Handoff closeout issued and on file",
            "No open issues in the test log",
        ],
        "next_hardening_step": "Use the kit on a real Lead & Contact Setup delivery. Complete the routing test script for all active channels. Promote to verification once one delivery is cleanly closed out.",
        "ownership_mode": "hybrid",
        "support_policy_key": "optional_support",
        "support_summary": "Works as fixed setup with optional support if the owner wants Drew to keep it maintained.",
        "rollback_plan": [],
    },
    "basic_cleanup": {
        "label": "Basic Cleanup",
        "type": "bundle",
        "offer_type": "public",
        "build_status": "hardening",
        "launch_eligible": False,
        "target_build_status": "ready",
        "kit_key": "basic_cleanup_v1",
        "kit_version": "v1",
        "current_truth_note": "Bundle-level operator docs now exist: scope matrix, activation checklist, and closeout template. Depends on Presence Refresh component kit. Neither the bundle nor the component is delivery-proven yet.",
        "target_truth_note": "Ready once Presence Refresh is delivery-proven and the bundle has been used for one real Basic Cleanup engagement.",
        "summary": "A fast-win presence cleanup using the Presence Refresh backbone with a narrower scope ceiling.",
        "includes": [
            "Fast-win Presence Refresh scope",
            "Tighter revision window",
        ],
        "required_artifacts": [
            "Same base presence assets as Presence Refresh",
        ],
        "access_requirements": [
            "Same access as Presence Refresh",
        ],
        "qa_checks": [
            "Scope matrix completed within Basic Cleanup ceiling",
            "Fast-win presence checks passed",
            "Closeout snapshot stored",
        ],
        "definition_of_done": [
            "Scope matrix completed and operator-reviewed",
            "Presence fast wins complete within scope ceiling",
            "Activation checklist completed",
            "Closeout template filled and on file",
        ],
        "missing_artifacts": [],
        "missing_qa": [],
        "missing_closeout": [],
        "missing_rollback": [],
        "artifact_files": {
            "bundle_scope_matrix": "lead_engine/delivery_kits/basic_cleanup/bundle_scope_matrix.md",
            "activation_checklist": "lead_engine/delivery_kits/basic_cleanup/activation_checklist.md",
            "closeout_template": "lead_engine/delivery_kits/basic_cleanup/closeout_template.md",
        },
        "promotion_criteria": [
            "Presence Refresh component kit delivery-proven",
            "Bundle used on at least one real Basic Cleanup engagement",
            "Scope stayed within defined ceiling",
            "Closeout template filled and on file",
        ],
        "next_hardening_step": "Deliver one real Presence Refresh, then use the Basic Cleanup scope matrix to run a narrower version. Fill the closeout template for that delivery.",
        "ownership_mode": "client_owned",
        "support_policy_key": "optional_support",
        "support_summary": "One-time cleanup with optional support after delivery.",
        "rollback_plan": [],
    },
    "presence_website": {
        "label": "Presence + Website",
        "type": "bundle",
        "offer_type": "public",
        "build_status": "hardening",
        "launch_eligible": False,
        "target_build_status": "ready",
        "kit_key": "presence_website_v1",
        "kit_version": "v1",
        "current_truth_note": "Bundle-level operator docs now exist: combined intake worksheet, dependency checklist, combined go-live checklist, and bundle closeout template. Component kits (Presence Refresh, Starter Website) are on disk but not delivery-proven yet.",
        "target_truth_note": "Ready once both component kits are delivery-proven and the bundle has been used for one real combined engagement.",
        "summary": "Combined presence cleanup and one-page website delivery under one intake and go-live sequence.",
        "includes": [
            "Presence Refresh",
            "Starter Website",
            "Combined go-live and handoff",
        ],
        "required_artifacts": [
            "Presence assets",
            "Website content/assets",
        ],
        "access_requirements": [
            "Presence account access",
            "Domain/hosting access",
        ],
        "qa_checks": [
            "All component dependency gates cleared",
            "Presence checks passed",
            "Website checks passed",
            "Cross-channel consistency reviewed",
            "Combined go-live checklist completed",
        ],
        "definition_of_done": [
            "Combined intake worksheet completed with owner",
            "All component dependencies confirmed via dependency checklist",
            "Presence complete per component kit",
            "Website live per component kit",
            "Combined go-live checklist completed",
            "Bundle closeout template filled and delivered to owner",
        ],
        "missing_artifacts": [],
        "missing_qa": [],
        "missing_closeout": [],
        "missing_rollback": [],
        "artifact_files": {
            "bundle_intake_worksheet": "lead_engine/delivery_kits/presence_website/bundle_intake_worksheet.md",
            "dependency_checklist": "lead_engine/delivery_kits/presence_website/dependency_checklist.md",
            "combined_go_live_checklist": "lead_engine/delivery_kits/presence_website/combined_go_live_checklist.md",
            "bundle_closeout_template": "lead_engine/delivery_kits/presence_website/bundle_closeout_template.md",
        },
        "promotion_criteria": [
            "Both component kits (Presence Refresh, Starter Website) delivery-proven",
            "Bundle used on at least one real combined engagement",
            "Combined go-live checklist completed without gaps",
            "Bundle closeout template filled and delivered to owner",
        ],
        "next_hardening_step": "Deliver one real Presence Refresh and one real Starter Website separately. Then use the bundle intake worksheet to run them as a combined engagement.",
        "ownership_mode": "hybrid",
        "support_policy_key": "optional_support",
        "support_summary": "Fixed project with optional post-launch support.",
        "rollback_plan": [],
    },
    "full_starter_package": {
        "label": "Full Starter Package",
        "type": "bundle",
        "offer_type": "public",
        "build_status": "hardening",
        "launch_eligible": False,
        "target_build_status": "ready",
        "kit_key": "full_starter_package_v1",
        "kit_version": "v1",
        "current_truth_note": "Bundle-level operator docs now exist: master intake worksheet and dependency sequencing checklist. All three component kits are on disk but not delivery-proven. Not ready to run as a combined delivery yet.",
        "target_truth_note": "Ready once all three component kits are delivery-proven and the full starter bundle has been used for one real combined engagement.",
        "summary": "Presence, one-page website, and lead/contact setup under one master activation packet.",
        "includes": [
            "Presence Refresh",
            "Starter Website",
            "Lead & Contact Setup",
        ],
        "required_artifacts": [
            "Presence assets",
            "Website content/assets",
            "Routing and notification preferences",
        ],
        "access_requirements": [
            "Presence account access",
            "Domain/hosting access",
            "Contact-routing access",
        ],
        "qa_checks": [
            "Presence checks passed",
            "Website checks passed",
            "Contact flow tested",
            "Master handoff complete",
        ],
        "definition_of_done": [
            "All component kits complete",
            "Cross-channel QA passed",
            "One final handoff delivered",
        ],
        "missing_artifacts": [],
        "missing_qa": [
            "Cross-offer QA sequence",
        ],
        "missing_closeout": [
            "Full starter package handoff packet",
        ],
        "missing_rollback": [],
        "artifact_files": {
            "master_intake_worksheet": "lead_engine/delivery_kits/full_starter_package/master_intake_worksheet.md",
            "dependency_sequencing_checklist": "lead_engine/delivery_kits/full_starter_package/dependency_sequencing_checklist.md",
        },
        "promotion_criteria": [
            "All three component kits (Presence Refresh, Starter Website, Lead & Contact Setup) delivery-proven",
            "Bundle used on at least one real full-starter engagement",
            "All three delivery phases complete in sequence",
            "One master handoff delivered to owner",
            "Cross-channel QA passed",
        ],
        "next_hardening_step": "Deliver each component kit separately first. Once all three are delivery-proven, run one client through the full starter bundle using the master intake worksheet.",
        "ownership_mode": "hybrid",
        "support_policy_key": "optional_support",
        "support_summary": "Fixed starter build with optional ongoing support.",
        "rollback_plan": [],
    },
    "missed_call_recovery": {
        "label": "Missed Call Recovery",
        "type": "module",
        "offer_type": "public",
        "build_status": "ready",
        "launch_eligible": True,
        "target_build_status": "ready",
        "kit_key": "missed_call_recovery_v1",
        "kit_version": "v1",
        "current_truth_note": "Real multi-client product with code, onboarding flow, pricing, proposal language, setup guide, and safe operational path already in repo.",
        "target_truth_note": "Keep as the launch benchmark for the rest of the public catalog.",
        "summary": "A Twilio-backed missed-call text-back flow with owner notification and lead logging.",
        "includes": [
            "Missed-call auto-response",
            "Owner notification",
            "Lead logging",
            "Go-live test",
        ],
        "required_artifacts": [
            "Voice greeting copy",
            "Auto-text copy",
            "Owner notification destination",
        ],
        "access_requirements": [
            "Twilio number/config",
            "Google Sheet or logging destination",
        ],
        "qa_checks": [
            "Missed-call response tested",
            "Owner notification tested",
            "Logging verified",
            "Safe-mode path documented",
        ],
        "definition_of_done": [
            "Twilio number/config ready",
            "Response path tested",
            "Owner notification tested",
            "Logging verified",
            "Rollback steps documented",
        ],
        "missing_artifacts": [],
        "missing_qa": [],
        "missing_closeout": [],
        "missing_rollback": [],
        "next_hardening_step": "Monitor as the reference ready module and use it to validate the rest of the hardening workflow.",
        "ownership_mode": "drew_managed",
        "support_policy_key": "managed_automation",
        "support_summary": "Managed automation with optional monthly support strongly recommended.",
        "rollback_plan": [
            "Disable auto-response send path",
            "Pause trigger or webhook handling",
            "Revert routing or destination if needed",
            "Log rollback note in Copperline",
        ],
    },
    "follow_up_reminder_setup": {
        "label": "Follow-Up & Reminder Setup",
        "type": "module",
        "offer_type": "public",
        "build_status": "hardening",
        "launch_eligible": False,
        "target_build_status": "ready",
        "kit_key": "follow_up_reminder_setup_v1",
        "kit_version": "v1",
        "current_truth_note": "Real kit files now exist: cadence worksheet, message template pack, access checklist, test sequence, and handoff closeout. Not yet proven in a live client delivery. This is a client-service setup kit — not the internal Copperline follow-up logic.",
        "target_truth_note": "Ready once the kit has been used for one real client delivery, all cadence stages tested, and closeout confirmed.",
        "summary": "A bounded reminder and follow-up setup for client businesses — approved templates, defined cadence, and a safe pause path.",
        "includes": [
            "Reminder cadence setup",
            "Approved message templates",
            "Test sequence",
            "Pause/rollback procedure",
        ],
        "required_artifacts": [
            "Reminder cadence choice",
            "Template copy approval",
            "Channel destination details",
        ],
        "access_requirements": [
            "Messaging or destination access",
        ],
        "qa_checks": [
            "Cadence defined and owner-reviewed",
            "All templates approved before go-live",
            "Each active reminder trigger tested",
            "Message arrives at correct destination",
            "Pause/disable path confirmed",
        ],
        "definition_of_done": [
            "Cadence worksheet completed and owner-reviewed",
            "All message templates approved by owner",
            "Access to send path confirmed",
            "Test sequence completed — all active stages pass",
            "Pause/disable path documented and confirmed",
            "Handoff closeout issued",
        ],
        "missing_artifacts": [],
        "missing_qa": [],
        "missing_closeout": [],
        "missing_rollback": [],
        "artifact_files": {
            "cadence_worksheet": "lead_engine/delivery_kits/follow_up_reminder_setup/cadence_worksheet.md",
            "message_template_pack": "lead_engine/delivery_kits/follow_up_reminder_setup/message_template_pack.md",
            "access_checklist": "lead_engine/delivery_kits/follow_up_reminder_setup/access_checklist.md",
            "test_sequence": "lead_engine/delivery_kits/follow_up_reminder_setup/test_sequence.md",
            "handoff_closeout": "lead_engine/delivery_kits/follow_up_reminder_setup/handoff_closeout.md",
        },
        "promotion_criteria": [
            "Kit used on at least one real client delivery",
            "Cadence and all active reminder triggers tested and passed",
            "Owner approved all message copy before go-live",
            "Handoff closeout issued and on file",
            "No open issues in the test log",
        ],
        "next_hardening_step": "Use the kit on a real Follow-Up & Reminder Setup delivery. Complete the test sequence for all active cadence stages. Promote to verification once one delivery is cleanly closed out.",
        "ownership_mode": "hybrid",
        "support_policy_key": "optional_support",
        "support_summary": "Can run as fixed setup with optional support when Drew is expected to maintain it.",
        "rollback_plan": [
            "Pause reminder trigger",
            "Disable outgoing reminder send",
            "Log follow-up rollback note",
        ],
    },
    "review_request_system": {
        "label": "Review Request System",
        "type": "module",
        "offer_type": "public",
        "build_status": "hardening",
        "launch_eligible": False,
        "target_build_status": "ready",
        "kit_key": "review_request_system_v1",
        "kit_version": "v1",
        "current_truth_note": "Real kit files now exist: review setup worksheet, review copy library, access checklist, QA checklist, and handoff closeout. Not yet proven in a live client delivery.",
        "target_truth_note": "Ready once the kit has been used for one real client delivery, test request completed, and closeout confirmed.",
        "summary": "A lightweight review-request workflow for client businesses — defined trigger rules, approved copy, and a safe pause path.",
        "includes": [
            "Review trigger rules",
            "Approved request copy library",
            "QA verification checklist",
            "Pause/rollback procedure",
        ],
        "required_artifacts": [
            "Review copy approval",
            "Review link destination",
            "Trigger rule choice",
        ],
        "access_requirements": [
            "Messaging or send path access",
            "Review profile link",
        ],
        "qa_checks": [
            "Review trigger defined and owner-reviewed",
            "Copy approved before any send",
            "Test request sent and confirmed delivered",
            "Review link points to correct profile",
            "Pause path documented and confirmed",
        ],
        "definition_of_done": [
            "Review setup worksheet completed with owner",
            "Copy library approved by owner before go-live",
            "Access to send path confirmed",
            "Test review request completed",
            "Review link verified at correct destination",
            "Pause/disable path documented and confirmed",
            "Handoff closeout issued",
        ],
        "missing_artifacts": [],
        "missing_qa": [],
        "missing_closeout": [],
        "missing_rollback": [],
        "artifact_files": {
            "review_setup_worksheet": "lead_engine/delivery_kits/review_request_system/review_setup_worksheet.md",
            "review_copy_library": "lead_engine/delivery_kits/review_request_system/review_copy_library.md",
            "access_checklist": "lead_engine/delivery_kits/review_request_system/access_checklist.md",
            "qa_checklist": "lead_engine/delivery_kits/review_request_system/qa_checklist.md",
            "handoff_closeout": "lead_engine/delivery_kits/review_request_system/handoff_closeout.md",
        },
        "promotion_criteria": [
            "Kit used on at least one real client delivery",
            "Test review request completed and delivered correctly",
            "Owner approved copy before go-live",
            "Handoff closeout issued and on file",
            "No open issues in the QA log",
        ],
        "next_hardening_step": "Use the kit on a real Review Request System delivery. Complete the QA checklist before sending to a real client. Promote to verification once one delivery is cleanly closed out.",
        "ownership_mode": "hybrid",
        "support_policy_key": "optional_support",
        "support_summary": "Can be set up once, with optional support if Drew keeps the cadence maintained.",
        "rollback_plan": [
            "Pause review-send trigger",
            "Disable review send path",
            "Log rollback note",
        ],
    },
    "estimate_job_status_communication": {
        "label": "Estimate & Job Status Communication",
        "type": "module",
        "offer_type": "public",
        "build_status": "hardening",
        "launch_eligible": False,
        "target_build_status": "ready",
        "kit_key": "estimate_job_status_communication_v1",
        "kit_version": "v1",
        "current_truth_note": "Real kit files now exist: status map worksheet, message template pack, access checklist, test sequence, and handoff closeout. Not yet proven in a live delivery.",
        "target_truth_note": "Ready once the kit has been used for one real client delivery, all status stages tested, and closeout confirmed.",
        "summary": "A contractor-safe communication module for estimates, approvals, and job-progress updates.",
        "includes": [
            "Status map",
            "Approved templates",
            "Test sequence",
        ],
        "required_artifacts": [
            "Status stages",
            "Template copy approval",
            "Send destinations",
        ],
        "access_requirements": [
            "Messaging or send path access",
        ],
        "qa_checks": [
            "Status map defines all active stages",
            "All templates approved by owner before go-live",
            "Each active stage tested — notification arrives at correct destination",
            "Copy matches approved template",
            "Safe-pause path documented and confirmed",
        ],
        "definition_of_done": [
            "Status map worksheet completed and owner-reviewed",
            "All active status stage templates approved by owner",
            "Access to send path confirmed",
            "Test sequence completed — all active stages pass",
            "Owner knows how to trigger each notification",
            "Safe-pause procedure documented",
            "Handoff closeout issued",
        ],
        "missing_artifacts": [],
        "missing_qa": [],
        "missing_closeout": [],
        "missing_rollback": [],
        "artifact_files": {
            "status_map_worksheet": "lead_engine/delivery_kits/estimate_job_status_communication/status_map_worksheet.md",
            "message_template_pack": "lead_engine/delivery_kits/estimate_job_status_communication/message_template_pack.md",
            "access_checklist": "lead_engine/delivery_kits/estimate_job_status_communication/access_checklist.md",
            "test_sequence": "lead_engine/delivery_kits/estimate_job_status_communication/test_sequence.md",
            "handoff_closeout": "lead_engine/delivery_kits/estimate_job_status_communication/handoff_closeout.md",
        },
        "promotion_criteria": [
            "Kit used on at least one real client delivery",
            "All active status stages tested and passed",
            "Owner approved all message copy before go-live",
            "Handoff closeout issued and on file",
            "No open issues in the test log",
        ],
        "next_hardening_step": "Use the kit on a real delivery. Complete the test sequence for all active status stages. Promote to verification once one delivery is cleanly closed out.",
        "ownership_mode": "hybrid",
        "support_policy_key": "optional_support",
        "support_summary": "Project setup with optional support for ongoing adjustments.",
        "rollback_plan": [
            "Pause estimate/job update trigger",
            "Disable outgoing updates",
            "Log rollback note",
        ],
    },
    "client_approval_estimate_portal": {
        "label": "Client Approval / Estimate Portal",
        "type": "module",
        "offer_type": "public",
        "build_status": "hardening",
        "launch_eligible": False,
        "target_build_status": "ready",
        "kit_key": "client_approval_estimate_portal_v1",
        "kit_version": "v1",
        "current_truth_note": "Real kit files now exist: approval flow worksheet, estimate page template, access checklist, QA verification checklist, and closeout/rollback doc. Not yet proven in a live delivery.",
        "target_truth_note": "Ready once the kit has been used for one real approval flow, the client responded via the correct path, and closeout was confirmed.",
        "summary": "A lightweight link-based approval flow for review, approve, confirm, and small uploads.",
        "includes": [
            "Approval link page",
            "Response capture",
            "Operator notification",
        ],
        "required_artifacts": [
            "Approval copy",
            "Estimate or approval content",
        ],
        "access_requirements": [
            "Hosting path for approval link",
            "Notification destination",
        ],
        "qa_checks": [
            "Estimate content is accurate — no placeholder text",
            "Approval link accessible on mobile",
            "Test response captured and Drew notified",
            "Approval window timing correct",
            "Deactivation path confirmed",
            "No sensitive data exposed beyond intended estimate",
        ],
        "definition_of_done": [
            "Approval flow worksheet completed",
            "Estimate content reviewed — real numbers, no placeholders",
            "Approval link or form accessible from a phone browser",
            "Test approval path verified",
            "Real client sent the approval link",
            "Client responded via correct path",
            "Drew notification received",
            "Link or form deactivated after approval",
            "Closeout log entry saved",
        ],
        "missing_artifacts": [],
        "missing_qa": [],
        "missing_closeout": [],
        "missing_rollback": [],
        "artifact_files": {
            "approval_flow_worksheet": "lead_engine/delivery_kits/client_approval_estimate_portal/approval_flow_worksheet.md",
            "estimate_page_template": "lead_engine/delivery_kits/client_approval_estimate_portal/estimate_page_template.md",
            "access_checklist": "lead_engine/delivery_kits/client_approval_estimate_portal/access_checklist.md",
            "qa_verification_checklist": "lead_engine/delivery_kits/client_approval_estimate_portal/qa_verification_checklist.md",
            "closeout_and_rollback": "lead_engine/delivery_kits/client_approval_estimate_portal/closeout_and_rollback.md",
        },
        "promotion_criteria": [
            "Kit used on at least one real approval flow",
            "Client responded via the correct approval path",
            "Drew notification received correctly",
            "Deactivation/expiry path confirmed after approval",
            "Closeout log entry on file",
        ],
        "next_hardening_step": "Use the kit on a real approval delivery. Complete the QA checklist before sending to a real client. Promote to verification once one approval flow is cleanly closed out.",
        "ownership_mode": "hybrid",
        "support_policy_key": "optional_support",
        "support_summary": "Lightweight approval links only. No account system or broad client dashboard.",
        "rollback_plan": [
            "Disable or expire approval link",
            "Revert linked action if needed",
            "Log rollback note",
        ],
    },
    "mobile_admin_workflow_helper": {
        "label": "Mobile Admin / owner workflow helper",
        "type": "module",
        "offer_type": "internal",
        "build_status": "hardening",
        "launch_eligible": False,
        "target_build_status": "ready",
        "kit_key": "mobile_admin_workflow_helper_v1",
        "kit_version": "v1",
        "current_truth_note": "Internal operator helper only. This is not a public sellable item.",
        "target_truth_note": "Ready when the internal consult-to-deploy operator flow is stable on mobile.",
        "summary": "An internal mobile-friendly operator toolset inside Copperline. This is not sold as a client-facing product.",
        "includes": [
            "Internal consult-to-deploy helper",
            "Phone-friendly operator actions",
        ],
        "required_artifacts": [],
        "access_requirements": [],
        "qa_checks": [
            "Usable on phone",
            "Supports consult-to-deploy workflow",
        ],
        "definition_of_done": [
            "Usable on phone",
            "Supports consult-to-deploy workflow",
            "No client-facing promise added",
        ],
        "missing_artifacts": [
            "Mobile-specific operator shortcuts",
        ],
        "missing_qa": [
            "Phone-size interaction pass",
        ],
        "missing_closeout": [],
        "missing_rollback": [],
        "next_hardening_step": "Use the new internal consult flow to harden the operator-only mobile path.",
        "ownership_mode": "drew_managed",
        "support_policy_key": "internal_only",
        "support_summary": "Internal operator helper only.",
        "rollback_plan": [],
    },
}


def _copy_list(values):
    return [deepcopy(value) for value in values]


def _merged_list(keys: list[str], field: str) -> list[str]:
    seen = set()
    out = []
    for key in keys:
        item = DELIVERY_CATALOG.get(key) or {}
        raw = item.get(field, [])
        values = raw if isinstance(raw, list) else ([raw] if isinstance(raw, str) and raw.strip() else [])
        for value in values:
            if value not in seen:
                seen.add(value)
                out.append(value)
    return out


def _main_stack_key(core_offer: str, bundle_key: str, selected_modules: list[str]) -> str:
    if bundle_key and bundle_key in DELIVERY_CATALOG:
        return bundle_key
    if core_offer and core_offer in DELIVERY_CATALOG:
        return core_offer
    for key in selected_modules:
        if key in DELIVERY_CATALOG:
            return key
    return ""


def stack_keys(core_offer: str, bundle_key: str, selected_modules: list[str]) -> list[str]:
    keys = []
    for key in [core_offer, bundle_key, *(selected_modules or [])]:
        if key and key in DELIVERY_CATALOG and key not in keys:
            keys.append(key)
    return keys


def _current_visibility(item: dict) -> str:
    if item.get("offer_type") == "internal":
        return "internal"
    return "ready" if item.get("launch_eligible") else "hidden"


def _target_visibility(item: dict) -> str:
    if item.get("offer_type") == "internal":
        return "internal"
    return "ready" if item.get("target_build_status") == "ready" else "hidden"


def _build_status_for_keys(keys: list[str]) -> str:
    return min(
        (DELIVERY_CATALOG[key]["build_status"] for key in keys),
        key=lambda value: BUILD_STATUS_ORDER.get(value, -1),
    )


def _offer_type_for_keys(keys: list[str]) -> str:
    return "internal" if any(DELIVERY_CATALOG[key]["offer_type"] == "internal" for key in keys) else "public"


def _launch_summary() -> dict:
    public_items = [item for item in DELIVERY_CATALOG.values() if item["offer_type"] == "public"]
    public_count = len(public_items)
    ready_count = sum(1 for item in public_items if item["build_status"] == "ready")
    hardening_count = sum(1 for item in public_items if item["build_status"] == "hardening")
    verification_count = sum(1 for item in public_items if item["build_status"] == "verification")
    unfinished = [item for item in public_items if not item["launch_eligible"]]
    return {
        "public_offer_count": public_count,
        "ready_count": ready_count,
        "hardening_count": hardening_count,
        "verification_count": verification_count,
        "launch_blocked": bool(unfinished),
        "unfinished_public_offers": len(unfinished),
    }


def get_catalog_payload() -> dict:
    entries = deepcopy(DELIVERY_CATALOG)
    for item in entries.values():
        item["current_visibility_state"] = _current_visibility(item)
        item["target_visibility_state"] = _target_visibility(item)
    public_modules = [
        key for key, item in entries.items()
        if item["type"] == "module" and item["offer_type"] == "public"
    ]
    hardening_items = [
        {
            "key": key,
            "label": item["label"],
            "type": item["type"],
            "offer_type": item["offer_type"],
            "build_status": item["build_status"],
            "launch_eligible": bool(item["launch_eligible"]),
            "current_truth_note": item.get("current_truth_note", ""),
            "target_truth_note": item.get("target_truth_note", ""),
            "missing_artifacts": _copy_list(item.get("missing_artifacts", [])),
            "missing_qa": _copy_list(item.get("missing_qa", [])),
            "missing_closeout": _copy_list(item.get("missing_closeout", [])),
            "missing_rollback": _copy_list(item.get("missing_rollback", [])),
            "artifact_files": dict(item.get("artifact_files", {})),
            "promotion_criteria": _copy_list(item.get("promotion_criteria", [])),
            "next_hardening_step": item.get("next_hardening_step", ""),
        }
        for key, item in entries.items()
    ]
    return {
        "prelaunch_mode": PRELAUNCH_MODE,
        "offer_types": deepcopy(OFFER_TYPES),
        "build_statuses": deepcopy(BUILD_STATUSES),
        "visibility_states": deepcopy(VISIBILITY_STATES),
        "global_policies": deepcopy(GLOBAL_POLICIES),
        "activation_packet_sections": _copy_list(ACTIVATION_PACKET_SECTIONS),
        "entries": entries,
        "public_module_keys": public_modules,
        "hardening_items": hardening_items,
        "launch_summary": _launch_summary(),
    }


def compute_stack_truth(core_offer: str, bundle_key: str, selected_modules: list[str]) -> dict:
    keys = stack_keys(core_offer, bundle_key, selected_modules)
    main_key = _main_stack_key(core_offer, bundle_key, selected_modules)
    if not keys or not main_key:
        return {
            "offer_type": "public",
            "build_status": "planned",
            "launch_eligible": False,
            "visibility_state": "hidden",
            "current_visibility_state": "hidden",
            "target_visibility_state": "hidden",
            "kit_key": "",
            "kit_version": "",
            "kit_status": "hidden",
            "required_artifacts": [],
            "access_requirements": [],
            "qa_checks": [],
            "rollback_plan": [],
            "activation_packet_sections": _copy_list(ACTIVATION_PACKET_SECTIONS),
            "definition_of_done": [],
            "ownership_mode": "",
            "support_policy_key": "",
            "support_summary": "",
            "current_truth_notes": [],
            "target_truth_notes": [],
            "missing_artifacts": [],
            "missing_qa": [],
            "missing_closeout": [],
            "missing_rollback": [],
            "next_hardening_steps": [],
        }

    main_item = DELIVERY_CATALOG[main_key]
    offer_type = _offer_type_for_keys(keys)
    build_status = _build_status_for_keys(keys)
    launch_eligible = offer_type == "public" and all(DELIVERY_CATALOG[key]["launch_eligible"] for key in keys)
    visibility_state = "internal" if offer_type == "internal" else ("ready" if launch_eligible else "hidden")
    target_visibility_state = "internal" if offer_type == "internal" else "ready"
    return {
        "offer_type": offer_type,
        "build_status": build_status,
        "launch_eligible": launch_eligible,
        "visibility_state": visibility_state,
        "current_visibility_state": visibility_state,
        "target_visibility_state": target_visibility_state,
        "kit_key": main_item["kit_key"],
        "kit_version": main_item["kit_version"],
        "kit_status": visibility_state,
        "required_artifacts": _merged_list(keys, "required_artifacts"),
        "access_requirements": _merged_list(keys, "access_requirements"),
        "qa_checks": _merged_list(keys, "qa_checks"),
        "rollback_plan": _merged_list(keys, "rollback_plan"),
        "activation_packet_sections": _copy_list(ACTIVATION_PACKET_SECTIONS),
        "definition_of_done": _merged_list(keys, "definition_of_done"),
        "ownership_mode": main_item.get("ownership_mode", ""),
        "support_policy_key": main_item.get("support_policy_key", ""),
        "support_summary": main_item.get("support_summary", ""),
        "current_truth_notes": _merged_list(keys, "current_truth_note"),
        "target_truth_notes": _merged_list(keys, "target_truth_note"),
        "missing_artifacts": _merged_list(keys, "missing_artifacts"),
        "missing_qa": _merged_list(keys, "missing_qa"),
        "missing_closeout": _merged_list(keys, "missing_closeout"),
        "missing_rollback": _merged_list(keys, "missing_rollback"),
        "next_hardening_steps": _merged_list(keys, "next_hardening_step"),
    }
