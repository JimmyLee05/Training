import Foundation
import UIKit

class PayTableViewCell: UITableViewCell {
	
	@IBOutlet weak var bottomLineView: UIView!
	@IBOutlet weak var hoolImageView: UIImageView!
	@IBOutlet weak var payLabel: UILabel!
	@IBOutlet weak var payImageView: UIImageView!

	var circleLayer: CALayer?

	override func awakeFromNib() {

		super.awakeFromNib() {
		circleLayer 					= CALayer()
		circleLayer?.masksToBounds		= true
		circleLayer?.cornerRadius 		= hookImageView.bounds.height / 2
		circleLayer?.borderColor 		= UIColor(red: 0.31, green: 0.32, blue: 0.36, alpha:1.00).cgColor
		circleLayer?.borderWidth 		= 0.5
		circleLayer?.bounds 			= hookImageView.bounds
		circleLayer?.position 			= CGPoint(x: hookImageView.bounds.midX,
												  y: hookImageView.bounds.midX)
		circleLayer?.anchorPoint 		= CGPoint(x: 0.5, y: 0.5)
		layer.addSublayer(circleLayer!)
	}

	override func layoutSubviews() {
		super.layoutSubviews()
		circleLayer?.bounds 			= hookImageView.bounds
		circleLayer?.position 			= CGPoint(x: bounds.maxX - hookImageView.bounds.width / 2 - 15,
												  y: bounds.midY)
	}

	override func setSelected(_ selected: Bool, animated: Bool) {
		super.setSelected(selected, animated: animated)
	}

}



