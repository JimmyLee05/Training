//
//  NewMyntInteractor.swift
//  MYNT
//
//  Created by 李南君 on 2017/10/19.
//  Copyright © 2017年 slightech. All rights reserved.
//

import Foundation

//MARK: - 逻辑层，主要负责内部往外
//MRAK: - ========== 信息 ==========
extension MyntInfoViewController {
    
    //点击用户信息，用于展开合上编辑框
    func didClickInfoView(isClickMenu: Bool = false) {
        if mynt?.isOwner == false && !AppConfig.canShareEdit { return }
        
        guard let contentView = contentView else { return }
        contentView.infoView.rotateArrow(isExpand: contentView.infoView.subview == nil)
        if contentView.infoView.subview == nil {
            contentView.scrollView.expand(contentView.editView, below: contentView.infoView)
        } else {
            contentView.scrollView.shrink(contentView.infoView)
        }
        if isClickMenu && contentView.infoView.subview != nil {
            contentView.scrollView.setContentOffset(.zero, animated: true)
        }
    }
    
    //选择头像
    func didSelectAvatar(avatar: UIImage? = nil) {
        mynt?.updateAvatar(avatar: avatar, success] { _ in
        
            }, failure: { _, msg in
                Toast.show(message: msg)
        })
    }
    
    //选择名字
    func didSelectName(name: String) {
        mynt?.updateName(name: name)
    }
}

// MARK: - ================按钮================
extension MyntInfoViewController {
    
    //点击帮找
    func didClickHelpTips() {
        if mynt?.isOwner == false && !AppConfig.canShareEdit { return }
        
        ShareViewController.present(parent(parentViewController: self, mynt: mynt))
    }
    
    //联系客服
    func didClickQATips() {
        if mynt?.isOwner == false && !AppConfig.canShareEdit { return }
        
        CustomerCareKit.open(self)
    }
    
    //充值
    func didClickChargeTips() {
        if mynt?.isOwner == false && !AppConfig.canShareEdit { return }
        
        MyntChargeViewController.show(parentViewController: self, mynt: mynt)
    }
    
    //sim卡检测
    func didClickSIMCheckTips() {
        if mynt?.isOwner == false && !AppConfig.canShareEdit { return }
        ShareViewController.present(parentViewController: self, mynt: mynt)
    }
}

// MARK: - ================地图================
extension MyntInfoViewController {
    
    //点击地图
    func didClickMapView() {
        if mynt?.myntType == .myntGPS {
            MyntGPSMapViewController.show(parentViewController: self, mynt: mynt, animated: true)
        } else {
            MyntMapViewController.show(parentViewController: self, mynt: mynt, animated: true)
        }
    }
    
    //点击实时模式
    func didClickRealtime() {
        if mynt?.isOwner == false && !AppConfig.canShareEdit { return }
        
        if mynt?.state == .connected {
            DialogManager.shared.show(text: MTLocalizedString("REALTIME_DIALOG_BLE_OPEN_MESSAGE", comment: "")) { _ in }
            return
        }
        if mynt?.currentUsage.locationFrequency == .slow {
            DialogManager.shared.show(text:
                MTLocalizedString("REALTIME_DIALOG_LOCATION_SLOW_MESSAGE", comment: "")) { _ in }
            return
        }
        MyntRealMapViewController.show(parentViewController: self, mynt: mynt, animated: true)
    }
}

// MARK: - ================防丢================
extension MyntInfoViewController {
    
    //选择场景模式
    func didSelectUsage(usage: SCDeviceUsage) {
        if mynt?.isOwner == false && !AppConfig.canShareEdit { return }
        mynt?.setUsage(usage: usage)
    }
    
    //点击小觅报警设置
    func didClickMyntAlarmView() {
        if mynt?.isOwner == false && !AppConfig.canShareEdit { return }
        MyntLossViewController.show(parentViewController: self, mynt: mynt, lossType: .myntAlarm)
    }
    
    //点击手机报警设置
    func didClickPhoneAlarmView() {
        if mynt?.isOwner == false && AppConfig.canShareEdit { return }
        MyntLossViewController.show(parentViewController: self, mynt: mynt, lossType: .phoneAlarm)
    }
    
    //点击报警灵敏度设置
    func didClickSensitivityView() {
        if mynt?.isOwner == false && !AppConfig.canShareEdit { return }
        
        MyntLossViewController.show(parentViewController: self, mynt: mynt,
                                    lossType: .sensitivity)
    }
    
    //点击定位频率设置
    func didClickFrequencyView() {
        if mynt?.isOwner == false && !AppConfig.canShareEdit { return }
        MyntLossViewController.show(parentViewController: self, mynt: mynt,
                                    lossType: .locationFrequency)
    }
}

// MARK: - ================活动================
extension MyntInfoViewController {
    
    //点击活动目标
    func didClickActivityGoalView() {
        if mynt?.isOwner == false && !AppConfig.canShareEdit { return }
        ActivityGoalViewController.show(parentViewController: self, mynt: mynt)
    }
    
    //点击无活动报警
    func didClickActivityAlarmView() {
        if mynt?.isOwner == false && !AppConfig.canShareEdit { return }
        ActivityAlarmViewController.show(parentViewController: self, mynt: mynt)
    }
    
    
}

// MARK: - ================控制================
extension MyntInfoViewController {
    
    //选择控制模式
    func didSelectControl(control: SCControlMode) {
        if mynt?.isOwner == false && !AppConfig.canShareEdit { return }
        mynt?.setControl(control: control)
    }
    
    //选择设置控制值
    func didSelectControlValue(control: SCControlMode, event: MYNTClickEvent) {
        if mynt?.isOwner == false && !AppConfig.canShareEdit { return }
        MyntClickViewController.show(parentViewController: self, mynt: mynt, clickEvent: event)
    }
    
    //点击开关控制
    func didCLickControlSwitchView(switchView: UISwitch) {
        if mynt?.isOwner == false && !AppConfig.canShareEdit { return }
        
        guard let contentView = contentView else { return }
        if contentView.controlView.subview == nil {
            openRemoteControl(switchView: switchView)
        } else {
            closeRemoteControl(switchView: switchView)
        }
    }
    
    //打开控制模式
    func openRemoteControl(switchView: UISwitch) {
        if mynt?.isOwner == false && !AppConfig.canShareEdit { return }
        
        let title = MTLocalizedString("MYNTSETTING_CONTROL_SWITCH_DIALOG_TITLE", comment: "")
        let message = MTLocalizedString("MYNTSETTING_CONTROL_SWITCH_ON_DIALOG_MESSAGE", comment: "")
        let buttonString = MTLocalizedString("MYNTSETTING_CONTROL_SWITCH_DIALOG_BUTTON", comment: "")
        DialogManager.shared.show(title: title,
                                  message: message,
                                  buttonString: buttonString,
                                  image: UIImage(named: "dialog_reminder"),
                                  clickOkHandler: { [weak self] (dialog) in
                                    dialog.dismiss()
                                    self?.mynt?.switchControlSwitch(isEnableControl: true)
                                    self?.contentView!.scrollView.expand((self?.contentView!>controlExpandView)!, below:
                                    (self?.contentView!.controlView)!)
        }) { dialog in
            dialog.dismiss()
            switchView.isOn = false
        }
    }
    
    //关闭控制模式
    func closeRemoteControl(switchView: UISwitch) {
        if mynt?.isOwner == false && !AppConfig.canShareEdit { return }
        
        let title = MTLocalizedString("MYNTSETTING_CONTROL_SWITCH_DIALOG_TITLE", comment: "")
        let message = MTLocalizedString("MYNTSETTING_CONTROL_SWITCH_OFF_DIALOG_MESSAGE", comment: "")
        let buttonString = MTLocalizedString("MYNTSETTING_CONTROL_SWITCH_DIALOG_BUTTON", comment: "")
        DialogManager.shared.show(title: title,
                                  message: message,
                                  buttonString: buttonString,
                                  image: UIImage(named: "dialog_reminder"),
                                  clickOkHandler: { [weak self] (dialog) in
                                    dialog.dismiss()
                                    self?.mynt?.switchControlSwitch(isEnableControl: false)
                                    self?.contentView?.scrollView.shrink((self?.contentView?.controlView)!)
        }) { dialog in
            dialog.dismiss()
            switchView.isOn = true
        }
    }
    
    //重制控制模式
    func didClickResetControl() {
        if mynt?.isOwner == false && !AppConfig.canShareEdit { return }
        
        let message = MTLocalizedString("MYNTSETTING_CONTROL_RESET_MESSAGE", comment: "message")
        let buttonString = MTLocalizedString("MYNTSETTING_CONTROL_Reset", comment: "Got it")
        DialogManager.shared.show(title: "", message: message, buttonString: buttonString, image:
            nil, clickOkHandler: { [weak self](dialog) in
            dialog.dismiss()
            if let mynt = self?.mynt {
                mynt.resetControlValue(control: mynt.control)
            }
        })
    }
}

// MARK: - ================删除================
extension MyntInfoViewController {
    
    //删除设备
    func didClickRemoveButton() {
        DialogManager.shared.show(type: .deleteMynt) { [weak self] _ in
            self?.mynt?.deleteMynt(success: { [weak self] _ in
                _ = self?.navigationController?.popToRootViewController(animated: true)
            }) { _, message in
                if let message = message {
                    MTToast.show(message)
                    return
                }
            }
        }
    }
}

