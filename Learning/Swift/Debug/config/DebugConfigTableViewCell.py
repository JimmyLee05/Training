import UIKit

class DebugConfigTableViewCell: UITableViewCell {
	
	@IBOutlet weak var nameLabel: UILabel!
	@IBOutlet weak var valueTextField: UITextField!
	var type = DebugConfigViewController.ConfigType.frequencyFast
	var doneHandler: ((DebugConfigViewController.ConfigType, Int) -> Void)?

	override func awakeFromNib() {
		super.awakeFromNib()
	}

	override func setSelected(_ selected: Bool, animated: Bool) {
		super.setSelected(selected, animated: animated)
	}
}

extension DebugConfigTableViewCell: UITextFieldDelegate {
	
	func textFielfShouldReturn(_ textField: UITextField) -> Bool {
		textField.resignFirstResponder()
		if let text = textField.text,
			let value = Int(text) {
			doneHandler?(type, value)
			} else {
				MTToast.show("请输入整型")
			}
			return true
	}
}