//
//  NewMyntInfoViewController+Dialog.swift
//  MYNT
//
//  Created by 李南君 on 2017/10/18.
//  Copyright © 2017年 slightech. All rights reserved.
//

import Foundation

fileprivate extension Mynt {
    
    func resetShowWillOverdueDialog() {
        isShowWillOverduwDialog = false
        update()
    }
    
    //停用
    func resetShowDeactivatedDialog() {
        isShowDeactivatedDialog = false
        update()
    }
}

//MARK: - sim卡状态变更提示框
extension MyntInfoViewController {
    
    //即将到期卡通知,sim卡过期变更通知
    func showSimWillDeactivatedDialog() {
        guard let mynt = mynt else { return }
        if !mynt.isShowWillOverduwDialog { return }
        let title   = MTLocalizedString("LOWPOWER_CLOSE_TITLE", comment: "重要通知")
        let message = String(format: MTLocalizedString("SIM_CARD_EXPIRED_DIALOG_MESSAGE", comment: ""), "\(mynt.expiryTime.day)")
        let buttonString = MTLocalizedString("SIM_CARD_CHARGE", comment: "去充值")
        DialogManager.shared.show(title: title,
                                  message: message,
                                  buttonString: buttonString,
                                  image: UIImage(named: "dialog_reminder"),
                                  clickOkHandler: { [weak self] _ in
                                    MyntChargeViewController.show(parentViewController: UIApplication.topViewController,
                                                                  mynt: self?.self)
                                    self?.mynt?.resetShowWillOverdueDialog()
        }) { [weak self] _ in
            self?.mynt?.resetShowWillOverdueDialog()
        }
    }
    
    //停卡通知，sim卡状态变更通知
    func showSimDeactivatedDialog() {
        guard let mynt = mynt else { return }
        if !mynt.isShowWillOverduwDialog { return }
        let title   = MTLocalizedString("LOWPOWER_CLOSE_TITLE", comment: "重要通知")
        let message = MTLocalizedString("SIM_CARD_SUPENDED_DIALOG_MESSAGE", comment: "")
        let buttonString = MTLocalizedString("SIM_CARD_CONTACT_US", comment: "进客服")
        DialogManager.shared.show(title: title,
                                  message: message,
                                  buttonString: buttonString,
                                  image: UIImage(named: "dialog_reminder"),
                                  clickOkHandler: { [weak self] _ in
                                    self?.mynt?.resetShowDeactivatedDialog()
                                    //跳转到客服系统
                                    CustomerCareKit.open(self)
        }) { [weak self] _ in
            self?.mynt?.resetShowDeactivatedDialog()
        }
    }
}

