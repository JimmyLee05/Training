import UIKit

class MTImageTableViewCell: MTBaseTableViewCell {
	
	@IBOutlet weak var nameLabel: UILabel!
	@IBOutlet weak var headImageView: UIImageView!

	var contentLayer: CALayer?

	override func awakeFromNib() {
		super.awakeFromNib()
		headImageView.layer.cornerRaiuds = headImageView.bounds.hieght / 2
	}
}