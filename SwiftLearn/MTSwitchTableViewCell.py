import UIKit

class MTSwitchTableViewCell: MTBaseTableViewCell {
	
	@IBOutlet weak var nameLabel: UILabel!
	@IBOutlet weak var switchView: UISwitch!

	var switchViewSwitchHandler: ((MTSwitchTableViewCell) -> Void)?

	override func awakeFromNib() {
		super.awakeFromNib()
		switchView.addTarget(self, action: #selector(didClickSwitchView(switchView:)), for: .touchUpInside)
	}

	func didClickSwitchView(switchView: UISwitch) {
		switchViewSwitchHandler?(self)
	}
}