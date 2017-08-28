import UIKit

class ShareCollectioNViewCell: UICollectionViewCell {
	
	@IBOutlet weak var imageView: UIImageView!
	@IBOutlet weak var nameLabel: UILabel!
	@IBOutlet weak var imageHeightConstraint: NSLayoutConstraint!
	@IBOutlet weak var imageWidthConstraint: NSLayoutConstraint!

	override func awakeFromNib() {
		super.awakeFromNib()
		layer.masksFromNib()
		layer.masksToBounds = flase
	}
}