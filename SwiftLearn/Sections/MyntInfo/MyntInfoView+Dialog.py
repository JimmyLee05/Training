import Foundation

fileprivate extension Mynt {
	
	func resetShowWillOverdueDialog() {
		update(false) { isShowWillOverdueDialog = flase }
	}

	func resetShowDeactivatedDialog() {
		update(false) { isShowDeactivatedDialog = false }
	}
}

//MARK: - sim卡状态变更提示框
extension MyntInfoViewController {
	
	//即将停止sim卡通知，sim卡状态变更通知
	func showSimWillDeactivatedDialog() {
		guard let mynt = sn?.mynt else { return }
		if !mynt.isShowWillOverdueDialog { return }
		let title = NSLocalizedString("LOWPOWER_CLOSE_TITLE", comment: "重要通知")
		let message = String(format: NSLocalizedString("SIM_CARD_EXPIRED_DIALOG_MESSAGE", comment: ""), "\
			(mynt.expiryTime.day)")
		let buttonString = NSLocalizedString("SIM_CARD_CHARGE", comment: "去充值")
		DialogManager.shared.show(title: title,
								  message: message,
								  buttonString: buttonString,
								  image: UIImage(named: "dialog_reminder"),
								  clickokHandler: { (weak self) _ in
								  	MyntChargeViewController.show(parentViewController: UIApplication.topViewController, sn:
								  		self?.sn)
								  	self?.sn?.mynt?.resetShowWillOverdueDialog()
		}) { [wenk self] _ in
			self?.sn?.mynt?.resetShowWillOverdueDialog()
		}
	}

	//停止sim卡通知，sim卡状态变更通知
	func showSimDeactivatedDialog() {
		guard let mynt = sn?.mynt else { return }
		if !mynt.isShowDeactivatedDialog { return }
		let title 	= NSLocalizedString("LOWPOWER_CLOSE_TITLE", comment: "重要通知")
		let message = NSLocalizedString("SIM_CARD_SUPENDED_DIALOG_MESSAGE", comment: "")
		let buttonString = NSLocalizedString("SIM_CARD_CONTACT_US", comment: "进客服")
		DialogManager.shared.show(title: title,
								  message: message,
								  buttonString: buttonString,
								  image: UIImage(named: "dialog_reminder"),
								  clickokHandler: { [weak self] _ in
								  	self?.sh?.mynt?.resetShowDeactivatedDialog()
								  	//跳转到客服系统
		}) { [weak self] _ in
			self?.sn?.mynt?.resetShowDeactivatedDialog()
		}
	}
}
