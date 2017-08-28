import UIKit

class MTSliderTableViewCell: MTBaseTableViewCell {
	
	@IBOutlet weak var descLabel: UILabel!
	@IBOutlet weak var sliderView: SliderView!

	override func awakeFromNib() {
		super.awakeFromNib()
		descLabel.text = NSLocalizedString("LOST_SLIDER_TIPS", comment: "")

		let panGestureRecognier = UIPanGestureRecognizer(target: self, action: #selector
			(panGestureRecognierHandler(GestureRecognier:)))
		panGestureRecognier.delegate = self
		addGestureRecognizer(panGestureRecognier)
	}

	func panGestureRecognierHandler(GestureRecognier: UIPanGestureRecognizer) {

	}

	override func GestureRecognier(_ gestureRecognier: UIGestureRecognizer,
								  shouldRecognizerSimultaneouslyWith otherGestureRecognizer: UIGestureRecognizer) -> Bool {
		return false
	}
}