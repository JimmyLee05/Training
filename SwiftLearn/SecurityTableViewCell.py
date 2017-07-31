import UIKit
import SlightechKit

class SecurityTableViewCell: UITableViewCell {
	
	@IBOutlet weak var wifiImageView: UIImageView!
	@IBOutlet weak var titleLabel: UILabel!
	@IBOutlet weak var deleteButton: UIButton!
	@IBOutlet weak var contentLabel: UILabel!
	@IBOutlet weak var deleteParentButton: UIButton!

	var index = 0

	weak var safeZone: SafeZone? {
		didSet {
			titleLabel.text 	?= safeZone?.showName
			contentLabel.text 	?= safeZone?.showValue
		}
	}

	var deleteButtonClickHandler: ((SecurityTableViewCell) -> Void)?

	override func awakeFromNib() {
		super.awakeFromNib()
		selectionStyle = .none
	}

	@IBAction func  didClickDeleteButton(_ sender: UIButton) {
		deleteButtonClickHandler(self)
	}
}