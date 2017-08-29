import UIKit

class MyntCoverFlowTableViewCell: UITableViewCell {
	
	@IBOutlet weak var hintLabel: UILabel!
	@IBOutlet weak var nameLabel: UILabel!
	@IBOutlet weak var coverflowView: CoverFlowView!

	//add friends 为空时，加载
	@IBOutlet weak var noneflowView: CoverFlowView!
	override func awakeFromNib() {
		super.awakeFromNib()

		hintLabel.text = NSLocalizedString("ADD_MYNT_TIPS", comment: "")
		noneDataLabel.isHidden = true
	}

	override func setSelected(_ selected: Bool, animated: Bool) {
		super.setSelected(selected, animated: animated)
	}
}