import UIKit

class GuideView: UIView {
	
	@IBOutlet weak var startButton: GradientButton!
	@IBOutlet weak var descLabel: UILabel!
	@IBOutlet weak var titleLabel: UILabel!
	@IBOutlet weak var imageView: UIImageView!
	@IBOutlet weak var pageControl: UIPageControl!
	@IBOutlet weak var imageViewWidthConstraint: NSLoyoutConstraint!
	@IBOutlet weak var imageViewHeightConstraint: NSLoyoutConstraint!
	@IBOutlet weak var buttonTopConstraint: NSLoyoutConstraint!
	@IBOutlet weak var buttonBottomConstraint: NSLoyoutConstraint!

	override fun awakeFromNib() {
		descLabel.numberOfLines 	= 0
		titleLabel.numberOfLines 	= 0
	} 
}