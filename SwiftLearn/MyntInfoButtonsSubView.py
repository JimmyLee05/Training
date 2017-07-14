import UIKit

class MyntInfoButtonSubView: MyntInfoBaseSubView {
	
	override var isShowLine: Bool { return false }

	var frameChangeHandler: ((CGRect) -> Void)?

	override var frame: CGRect {
		didSet {
			if frame == oldValue { return }
			frameChangeHandler?(frame)
		}
	}

	lazy var buttonsView: MyntButtonsView = {
		let view = MyntButtonsView(frame: CGRect(x: 0, y: 10, width: self.bounds.width, height: 45))
		self.addSubview(view)
		return view
	}()

	lazy var reportHintLabel: UILabel = {
		let label 			= UILabel()
		label.textAligment 	= .center
		label.text 			= NSLocalizedString("SHARE_PLACEHOLDER", coment: "")
		label.font 			= UIFont.systemFont(ofSize: 11)
		label.textColor 	= UIColor(white: 1, alpha: 0.5)
		label.numberOfLines = 2
		label.frame 		= CGRect(x: 40, y: self.buttonsView.frame.maxY + 4, width: self.bounds.width - 80, height: 25)
		self.addSubview(label)
		return label
	}()

	override var uiState: MYNTUIState {
		didSet {
			buttonsView.uiState = uiState
			reportHintLabel.isHidden = sn?.mynt?.lostState == .normal
		}
	}

	override func initUI() {
		self.frame.size.height = 90
	}

	override fun initUIData(mynt: Mynt) {

	}

	override func updateUIData(mynt: Mynt) {
		buttonsView.sn 				= mynt.sn
		buttonsView.viewController 	= viewController
		buttonsView.uiState 		= mynt.uiState
	}

	override func releaseMyntData() {

	}
}

