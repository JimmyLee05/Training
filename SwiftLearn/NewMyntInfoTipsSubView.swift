//
//  NewMyntInfoTipsSubView.swift
//  MYNT
//
//  Created by 李南君 on 2017/10/27.
//  Copyright © 2017年 slightech. All rights reserved.
//

import UIKit

class MyntInfoTipsSubView: MyntInfoBaseSubView {
    
    enum Tips {
        
        case none
        
        case phoneAlarm
        case myntAlarm
        case map
        case report
        case askhelp
        
        case simDeactivated
        case simNotInsert
        case simNetError
        case simOverdue
        case lowPower
        case disconnected
        case trackGPS
        
        var desc: String {
            switch self {
            case .myntAlarm: return MTLocalizedString("MYNTSETTING_TIPS_ALARM_DESC", comment: "")
            case .phoneAlarm: return MTLocalizedString("MYNTSETTING_TIPS_RING_DESC", comment: "")
            case .map: return MTLocalizedString("MYNTSETTING_TIPS_MAP_DESC", comment: "")
            case .report: return MTLocalizedString("MYNTSETTING_TIPS_REPORTLOST_DESC", comment: "")
            case .askhelp: return MTLocalizedString("MYNTSETTING_TIPS_ASKHELP_DESC", comment: "")
                
            case .simDeactivated: return MTLocalizedString("GPS_TIPS_SIM_STOP", comment: "")
            case .simNotInsert: return MTLocalizedString("GPS_TIPS_NOSIM", comment: "")
            case .simNetError: return MTLocalizedString("GPS_TIPS_SIM_ERROR", comment: "")
            case .simOverdue: return MTLocalizedString("GPS_TIPS_OVER15", comment: "")
            case .lowPower: return MTLocalizedString("GPS_TIPS_LOWPOWER1", comment: "")
            case .disconnected: return MTLocalizedString("GPS_TIPS_OFFLINE", comment: "")
            case .trackGPS: return MTLocalizedString("GPS_TIPS_PATH", comment: "")
            default: return ""
            }
        }
        
        var buttonString: String {
            switch self {
            case .askhelp: return MTLocalizedString("MYNTSETTING_TIPS_ASKHELP_BUTTON", comment: "")
            case .simDeactivated: return MTLocalizedString("GPS_TIPS_CONTACT", comment: "")
            case .simNetError: return MTLocalizedString("GPS_TIPS_TOOL", comment: "")
            case .simOverdue: return MTLocalizedString("GPS_TIPS_CHARGECENTER", comment: "")
            default: return ""
            }
        }
        
        
    }
}





