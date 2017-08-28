import UIKit

class MTBaseTableViewCell: UITableViewCell {
	
	//用于记录，读数
	var obj: Any?

	override func awakeFromNib() {
		super.awakeFromNib()
		selectionStyle 		= .none
		backgroundColor 	= UIColor.clear
	}
}