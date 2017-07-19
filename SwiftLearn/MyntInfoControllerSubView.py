import UIKit

class MyntInfoControllerSubView: MyntInfoBaseSubView {
	
	lazy var switchView: MyntInfoSettingSwitchView = {
		let view 	= MyntInfoSettingSwitchView()
		view.frame 	= CGRect(x: 0, y: self.messageLabel.frame.maxY + 30, width: self.bounds.width,
			height: 55)
		self.addSubview(view)
		return view
	}()

	override var isShowLine: Bool { return false }

	override func initUI() {
		titleLabel.text 	= NSLocalizedString("MYNTSETTING_CONTROL_TITLE", comment: "")
		messageLabel.text 	= NSLocalizedString("MYNTSETTING_CONTROL_DESC", comment: "")
	}

	override func initUIData(mynt: Mynt) {

	}

	override func updateUIData(mynt: Mynt) {
		let software = NSString(format: "%@", mynt.software).integerValue

		let myntShowSwitch = mynt.myntType == .mynt && software >= 29
		let myntGPSShowSwitch = mynt.myntType == .myntGPS
		let showSwitch = myntShowSwitch || myntGPSShowSwitch

		switchView.titleLabel.text = NSLocalizedString("MYNTSETTING_CONTROl_SWITCH_TITLE", comment:
			"")
		switchView.switchView.isOn = mynt.isEnableControl
		switchView.isHidden = !showSwitch
		self.frame.size.height = (showSwitch ? switchView.frame.maxY : messageLabel.frame.maxY) + 15
		switchView.switchView.addTarget(self, action: #selector(didClickSwitch(switchView:)), for: .touchUpInside)
	}

	override func releaseMyntData() {

	}

	@objc fileprivate func didClickSwitch(switchView: UISwitch) {
		viewController?.didClickControllerSwitchView(switchView: switchView)
	}
}
