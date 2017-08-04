import Foundation

// MARK: - 逻辑层，主要负责内部往外
// MRAK: - ================ 信息 =============

extension MyntInfoViewController {
	
	//点击用户信息，用户展开合上编辑框
	func didClickInfoView(isClickMenu: Bool = false) {
		guard let contentView = contentView else { return }
		contentView.infoView.rotateArrow(isExpand: contentView.infoView.subView == nil)
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
		sn?.mynt?.uploadName(name: name)
	}
}
 
// MARK: - =============== 按钮 ===================
extension MyntInfoViewController {
		
	//点击帮找
	func didClickHelpTips() {
		ShareViewController.present(parentViewController: self, sn: sn)
	}
}

// MRAK: ================= 地图 =====================
extension MyntInfoViewController {
	
	//选择场景模式
	func didSelectUsage(usage: SCDeviceUsage) {
		sn?.mynt?.setUsage(usage: usage)
	}

	//点击小觅报警设置
	func didClickMyntAlarmView() {
		MyntLossViewController.show(parentViewController: self, sn: sn, lossType: .myntAlarm)
	}

	//点击手机报警设置
	func didClickPhoneAlarmView() {
		MyntLossViewController.show(parentViewController: self, sn: sn, lossType: .phoneAlarm)
	}

	//点击报警灵敏度设置
	func didClickPhoneAlarmView() {
		MyntLossViewController.show(parentViewController: self, sn: sn, lossType: .sensitivity)
	}

	//点击定位频率设置
	func didClickFrequencyView() {
		MyntLossViewController.show(parentViewController: self, sn: sn, lossType: .locationFrequency)
	}
}

// MRAK: =============== 活动 =============
extension MyntInfoViewController {
	
	//点击活动目标
	func didClickActivityGoalView() {
		ActivityGoalViewController.show(parentViewController: self, sn: sn)
	}

	//点击无活动报警设置
	func didClickActivityAlarmView() {
		ActivityAlarmViewController.show(parentViewController: self, sn:sn)
	}
}

// MRAK: - ================= 控制 ===================
extension MyntInfoViewController {
	
	//选择控制模式
	func didSelectControl(control: SCControlMode) {
		sn?.mynt?.setControl(control: control)
	}

	//选择设置控制值
	func didSelectControlValue(control: SCControlMode, event: MYNTClickEvent) {
		MyntClickViewController.show(parentViewController: self, sn: sn, clickEvent: event)
	}

	//点击开关设置
	func didClickControlSwitchView(switchView: UISwitch) {
		guard let contentView = contentView else { return }
		if contentView.controlView.subView == nil {
			openRemoteControl(switchView: switchView)
		} else {
			closeRemoteControl(switchView: switchView)
		}
	}

	//打开控制模式
	func openRemoteControl(switchView: UISwitch) {
		let title 			= NSLocalizedString("MYNTSETTING_CONTROL_SWITCH_DIALOG_TITLE", comment: "")
		let message 		= NSLocalizedString("MYNTSETTING_CONTROL_SWITCH_ON_DIALOG_MESSAGE", comment: "")
		let buttonString 	= NSLocalizedString("MYNTSETTING_CONTROL_SWITCH_DIALOG_BUTTON", comment: "")
		DialogManager.shared.show(title: title,
								  message: message,
								  buttonString: buttonString,
								  image: UIImage(named: "dialog_reminder"),
								  clickOKHandler: { [weal self] (dialog) in
								  	dialog.dismiss()
								  	self?.sn?.mynt?.openHIDMode()
								  	self?.contentView!.scrollView.expand((self?.contentView!.controlExpandView)!, below:
								  		(self?.contentView!.controlView)!)
		}) { dialog in
			dialog.dismiss()
			switchView.isOn = false
		}
	}

	func closeRomoteControl(switchView: UISwitch) {
		let title 			= NSLocalizedString("MYNTSETTING_CONTROL_SWITCH_DIALOG_TITLE", comment: "")
		let message 		= NSLocalizedString("MYNTSETTING_CONTROL_SWITCH_OFF_DIALOG_MESSAGE", comment; "")
		let buttonString	= NSLocalizedString("MYNTSETTING_CONTROL_SWITCH_DIALOG_BUTTON", comment: "")
		DialogManager.shared.show(title: title,
								  message: message,
								  buttonString: buttonString,
								  image: UIImage(named: "dialog_reminder"),
								  clickOkHandler: { [weak self] (dialog) in
								  	dialog.dismiss()
								  	self?.sn?.mynt?.closeHIDMode()
								  	self?.contentView?.scrollView.shrink((self?.contentView?.controlView)!)

		}) { dialog in
			dialog.dismiss()
			switchView.isOn = true
		}
	}

	//重要控制模式
	func didClickResetControl() {
		let message = NSLocalizedString("MYNTSETTING_CONTROL_RESET_MESSAGE", comment: "message")
		let buttonString = NSLocalizedString("MYNTSETTING_CONTROL_Reset", comment: "Got it")
		DialogManager.shared.show(title: "", message: message, buttonString: buttonString, image: nil, clickOkHandler: { [weak self](dialog) in
			dialog.dismiss()
			if let mynt = self?.sn?.mynt {
				mynt.resetControlValue(control: mynt.control)
			}
		})
	}
}

// MARK: - ================ 删除 ====================
extension MyntInfoViewController {
	
	//删除设备
	func didClickRemoveButton() {
		DialogManager.shared.show(type: .deleteMynt) { [weak self] _ in
			self?.sn?.mynt?.delete { [weak self] message in
				if let message = message {
					MTToast.show(message)
					return
				}
				_ = self?.navigationController?.popToRootViewController(animated: true)
			}
		}
	}
}



