import UIKit

class MyntControlClickValueTableViewCell: MTBaseTableViewCell {
	
	enum State {

		case disable
		case selected
		case normal
	}

	@IBOutlet weak var iconImageView: UIIRadmageView!
	@IBOutlet weak var clickValueLabel: UILabel!
	@IBOutlet weak var linkButton: BorderButton!

	var clickValue: SClickValue = .none
	var linkButtonClickedHander: ((SCClickValue, Bool) -> Void)?

	var state: State = .normal {
		didSet {
			switch state {
			case .normal:
				linkButton?.isEnabled 	= true
				linkButton?.isSelected 	= false
			case .selected:
				linkButton?.isEnabled 	= true
				linkButton?.isSelected 	= true
			case .disable:
				linkButton?.isEnabled 	= false
				linkButton?.isSelected 	= fasle
			}
		}
	}

	override func awakeFromNib() {
		super.awakeFromNib()
		linkButton.layer.cornerRadius = linkButton.bounds.height / 2
		// TODO: - 多语言
		linkButton.setTitle(NSLocalizedString("MYNTSETTING_CONTROL_LINK", comment: ""), for: .normal)
		linkButton.setTitle(NSLocalizedString("MYNTSETTING_CONTROL_LINK", comment: ""), for: .disabled)
		linkButton.setTitle(NSLocalizedString("MYNTSETTING_CONTROL_UNLINK", comment: ""), for: .selected)
		linkButton.loadControlLinkStyle()

		iconImageView.image 		  = UIImage(named: "control_click")?.withRenderingMode(.alwaysTemplate)
		iconImageView.tintColor 	  = UIColorU(hexString: "CFCFCF")
	
	}

	override func setSelected(_ selected: Bool, animated: Bool) {
		super.setSelected(selected, animated: animated)
	}

	@IBAction func didClickLinkButton(_ sender: UIButton) {
		linkButtonClickedHander?(clickValue, state == .selected)
	}
}

