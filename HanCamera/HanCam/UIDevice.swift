//
//  UIDevice.swift
//  HanCam
//
//  Created by 李南君 on 2018/9/26.
//  Copyright © 2018 NanJun Li. All rights reserved.
//

import UIKit
import SystemConfiguration.CaptiveNetwork
import CoreTelephony.CTCarrier
import CoreTelephony.CTTelephonyNetworkInfo

public extension UIDevice {

    public enum ScreenType {
        case iphone4
        case iphone5
        case iphone6
        case iphone6p
        case iphonex
        case iphonexr
    }

    // 判断屏幕类型
    public static var screenType: ScreenType {
        let screenWidth = UIScreen.main.bounds.width
        let screenHeight = UIScreen.main.bounds.height

        switch (screenWidth, screenHeight) {
        case (320, 480), (480, 320):
            return .iphone4
        case (320, 568), (568, 320):
            return .iphone5
        case (375, 667), (667, 375):
            return .iphone6
        case (414, 736), (736, 414):
            return .iphone6p
        case (375, 812), (812, 375):
            return .iphonex
        case (414, 896), (896, 414):
            return .iphonexr
        default:
            return .iphone6
        }
    }

    // 是否是刘海屏
    public static var isNotchScreen: Bool {
        return isPhoneX || isPhoneXR
    }

    // 是否是iPhone X
    public static var isPhoneX: Bool {
        return UIDevice.screenType == .iphonex
    }

    // 是否是iPhone XR
    public static var isPhoneXR: Bool {
        return UIDevice.screenType == .iphonexr
    }

    // 设备名
    public static var modelName: String {
        var systemInfo = utsname()
        uname(&systemInfo)
        let machineMirror = Mirror(reflecting: systemInfo.machine)
        let identifier = machineMirror.children.reduce("") { identifier, element in
            guard let value = element.value as? Int8 , value != 0 else { return identifier }
            return identifier + String(UnicodeScalar(UInt8(value)))
        }

        switch identifier {
        case "iPod5,1":                                 return "iPod Touch 5"
        case "iPod7,1":                                 return "iPod Touch 6"
        case "iPhone3,1", "iPhone3,2", "iPhone3,3":     return "iPhone 4"
        case "iPhone4,1":                               return "iPhone 4s"
        case "iPhone5,1", "iPhone5,2":                  return "iPhone 5"
        case "iPhone5,3", "iPhone5,4":                  return "iPhone 5c"
        case "iPhone6,1", "iPhone6,2":                  return "iPhone 5s"
        case "iPhone7,2":                               return "iPhone 6"
        case "iPhone7,1":                               return "iPhone 6 Plus"
        case "iPhone8,1":                               return "iPhone 6s"
        case "iPhone8,2":                               return "iPhone 6s Plus"
        case "iPhone8,4":                               return "iPhone SE"
        case "iPhone9,1", "iPhone9,3":                  return "iPhone 7"
        case "iPhone9,2", "iPhone9,4":                  return "iPhone 7 Plus"
        case "iPhone10,1", "iPhone10,4":                return "iPhone 8"
        case "iPhone10,2", "iPhone10,5":                return "iPhone 8 Plus"
        case "iPhone10,3", "iPhone10,6":                return "iPhone X"
        case "iPad2,1", "iPad2,2", "iPad2,3", "iPad2,4":return "iPad 2"
        case "iPad3,1", "iPad3,2", "iPad3,3":           return "iPad 3"
        case "iPad3,4", "iPad3,5", "iPad3,6":           return "iPad 4"
        case "iPad4,1", "iPad4,2", "iPad4,3":           return "iPad Air"
        case "iPad5,3", "iPad5,4":                      return "iPad Air 2"
        case "iPad2,5", "iPad2,6", "iPad2,7":           return "iPad Mini"
        case "iPad4,4", "iPad4,5", "iPad4,6":           return "iPad Mini 2"
        case "iPad4,7", "iPad4,8", "iPad4,9":           return "iPad Mini 3"
        case "iPad5,1", "iPad5,2":                      return "iPad Mini 4"
        case "iPad6,3", "iPad6,4", "iPad6,7", "iPad6,8":return "iPad Pro"
        case "AppleTV5,3":                              return "Apple TV"
        case "i386", "x86_64":                          return "Simulator"
        default:                                        return identifier
        }
    }

}


