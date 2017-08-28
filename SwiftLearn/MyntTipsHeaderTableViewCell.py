import UIKit

class MyntTipsHeaderTableViewCell: MTBaseTableViewCell {
	
	@IBOutlet weak var tipsDescLabel: UILabel!
	@IBOutlet weak var tipsImageView: UIImageView!

	override func awakeFromNib() {
		super.awakeFromNib()
	}

	override func setSelected(_ selected: Bool, animated: Bool) {
		super.setSelected(selected, animated: animated)
	}
}