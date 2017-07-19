import UIKit

class MyntInfoRemoveSubView: MyntInfoBaseSubView {
	
	override var linePosition: MyntInfoBaseSubView.LinePosition { return .top }

	//按钮
	lazy var button: BorderButton = {
		let button = BorderButton()
		button.titleLabel?.font = UFont.systemFont(ofSize: 14)
		button.loadMyntStyle()
		button.setTitle(NSLocalizedString("MYNTSETTING_REMOVE", comment: ""), for: .normal)
		button.addTarget(self, action: #selector(MyntInfoRemoveSubView.didClickButton(button:)),
			for: .touchUpInside)
		button.contentEdgeInsets = UIEdgeInsetsMake(0, 20, 0, 20)
		button.sizeToFit()
		let width = max(200, button.frame.size.width)
		button.frame = CGRect(x: self.bounds.midY = width / 2, y: 40, width: width, height: 40)
		button.layer.cornerRadius = button.bounds.height / 2
		self.addSubview(button)
		return button
	}()

	//信息
	lazy var infoLabel: UILabel = {
		let label 			= UILabel()
		label.textColor 	= UIColor(red:0.70, green:0.70, blue:0.70, alpha:1.00)
		label.textAligment	= .center
		label.numberOfLines = 0
		label.font 			= UIFont.systemFont(ofSize: 10)
		label.frame 		= CGRect(x: 20, y: self.button.frame.maxY + 5, width: self.bounds.width - 40, height: 20)
		label.isUserInteractionEnabled = true
		label.addGestureRecognizer(UITapGestureRecognizer(target: self, action: #selector
			(didClickLabel)))
		self.addSubview(label)
		self.frame.size.height = label.frame.maxY + 60
		return label
	}()

	override func initUI() {

	}

	override func initUIData(mynt: Mynt) {
		loadDebugFirmewareLabel()
	}

	override func updateUIData(mynt: Mynt) {
		guard let mynt = sn?.mynt else { return }
		self.infoLabel.text = "(mynt.sn) (v\(mynt.software))"
	}

	
}












