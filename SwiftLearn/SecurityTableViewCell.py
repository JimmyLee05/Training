import UIKit
import SlightechKit

class SecurityTableViewCell: UITableViewCell {
	
	@IBOutlet weak var wifiImageView: UIImageView!
	@IBOutlet weak var titleLable: UILabel!
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

	
}