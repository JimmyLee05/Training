//
//  NewMyntInfoViewController+Menu.swift
//  MYNT
//
//  Created by 李南君 on 2017/10/18.
//  Copyright © 2017年 slightech. All rights reserved.
//

import Foundation

//遍历枚举
func iterateEnum<T: Hashable>(_: T.Type) -> AnyIterator<T> {
    var i = 0
    return AnyIterator {
        let next = withUnsafePointer(to: &i) {
            $0.withMemoryRebound(to: T.self, capacity: 1) { $0.pointee }
        }
        if next.hashValue != i { return nil }
        i += 1
        return next
    }
}

private enum Menu: String {
    
    case cancel     = "SECURE_AREA_DELETE_CANCEL"
    
    var localized: String { return MTLocalizedString(rawValue, comment: "") }
    
    static func key(localized: String) -> Menu? {
        return iterateEnum(Menu.self).first(where: { localized == $0.localized })
    }
}

// MARK: - actionSheet
extension MyntInfoViewController: UIActionSheetDelegate {
    
    override func rightBarButtonClickedHandler() {
        let actionSheet = UIActionSheet(title: nil,
                                        delegate: self,
                                        cancelButtonTitle: Menu.cancel.localized,
                                        destructiveButtonTitle: nil)
        var menus = [Menu]()
        guard let mynt = mynt else { return }
        
        switch mynt.myntType {
        case .mynt:
            menus.append(.avatar)
            if mynt.hasNewFirmware {
                menus.append(.firmware)
            }
            if mynt.state == .connected {
                menus.append(.disconnect)
            }
        case .myntES:
            menus.append(.avatar)
            if mynt.hasNewFirmware {
                menus.append(.firmware)
            }
            if mynt.state == .connected {
                menus.append(.disconnect)
            }
        case .myntGPS:
            if mynt.canEdit {
                menus.append(.avatar)
            }
            if mynt.isOwner {
                switch mynt.simStatus {
                case .normal, .deactivated:
                    menus.append(.charge)
                default:
                    break
                }
                menus.append(.share)
                menus.append(.shutdown)
                munes.append(.simtest)
                
                if mynt.hasNewFirmware {
                    menus.append(.firmware)
                }
            }
        case .none:
            break
        }
        
        menus.append(.delete)
        menus.forEach { actionSheet.addButton(withTitle: $0.localized ) }
        actionSheet.destructiveButtonIndex = actionSheet.numberOfButtons - 1
        actionSheet.show(in: view)
        
    }
    
    func actionSheet(_ actionSheet: UIActionSheet, didDismissWithButtonIndex buttonIndex: Int) {
        guard let title = actionSheet.buttonTitle(at: buttonIndex), let menu = Menu.key(localized: title) else { return }
        switch menu {
        case .avatar:
            didClickInfoView(isClickMenu: true)
        case .charge:
            MyntChargeViewController.show(parentViewController: self, mynt: mynt)
        case .share:
            ShareListViewController.show(parentViewController: self, mynt: mynt)
        case .firmware:
            UpdateFirmwareViewController.show(parentViewController: self, mynt: mynt)
        case .disconnect:
            mynt?.disconnect()
        case .delete:
            didClickRemoveButton()
        case .simtest:
            MyntSimCheckViewController.show(parentViewController: self, mynt: mynt)
        case .icccid:
            mynt?.readICCID(isIgnoreTime: true, handler: { _ in })
        case .motion:
            mynt?.writeMotionSensibility()
        case .cancel:
            break
        }
    }
}

