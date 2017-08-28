import UIKit

class ChargeTableViewCell: UITableViewCell {
	
	//说明
	@IBOutlet weak var wxplainLabel: UILabel!
	//价格
	@IBOutlet weak var priceLabel: UILabel!
	//币种: 美元，人民币
	@IBOutlet weak var currentLabel: UILabel!

	@IBOutlet weak var sliderView: SliderView!
	override func awakeFromNib() {
		super.awakeFromNib()
		selectionStyle = .none

		[currentLabel, priceLabel].forEach { (label) in
			label?.textColor = ColorStyle.kBlueGradientColor.start

		}

		currentLabel.text 			= NSLocalizedString("¥", comment: "币种")
		explainLabel.textColor 		= UIColor(red: 120 / 255.0, green: 120 / 255.0, blue: 120 / 255.0, alpha: 1.0)
		let panGestureRecognizer 	= UIPanGestureRecognizer(target: self, action: #selector
			(panSGestureRecognizerHandler(gestureRecognizer:)))
		panGestureRecognizer.delegate = self
		addGestureRecognizer(panGestureRecognizer)
	}

	func panGestureRecognizerHandler(gestureRecognizer: UIPanGestureRecognizer) {

	}

	override func gestureRecognizer(_ gestureRecognizer: UIPanGestureRecognizer,
									shouldRecognizeSimultaneouslyWith otherGestureRecognizer: UIGestureRecognizer) -> Bool {
		return false
	} 
}


