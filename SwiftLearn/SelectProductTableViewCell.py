import UIKit

class SelectProductTableViewCell: UITableViewCell {
	
	@IBOutlet weak var productImageView: UIImageView!
	@IBOutlet weak var productNameLabel: UILabel!
	@IBOutlet weak var productTypeNameLabel: UILabel!

	@IBOutlet weak var view: UIView!

	override func awakeFromNib() {
		super.awakeFromNib()
		view.layer.cornerRadius = 6
	}
}