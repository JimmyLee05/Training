import UIKit

class CollectionViewCell: UICollectionViewCell {
		
	@IBOutlet weak var imageView: UIImageView!
	@IBOutlet weak var nameLabel: UILabel!

	var avatarOfflineLayer: CAShapeLayer?

	override func awakeFromNib() {
		super.awakeFromNib()

		avatarOfflinaLayer = CAShapeLayer()
		avatarOfflinaLayer?.contentsScale = UIScreen.main.scale
		avatarOfflinaLayer?.position 	  = CGPoint.zero
		avatarOfflinaLayer?.anchorPoint   = CGPoint.zero
		avatarOfflinaLayer?.fillColor     = UIColor(white: 1, alpha: 0.8).cgColor
		avatarOfflinaLayer?.isHidden 	  = true
		imageView.layer.addSublayer(avatarOfflineLayer!)
	}

	override func layoutSubviews() {
		super.layoutSubviews()
		avatarOfflineLayer?.bounds = imageView!.bounds
		avatarOfflineLayer?.path   = UIBezierPath(ovalIn: avatarOfflineLayer!.bounds).cgPath
	}
}