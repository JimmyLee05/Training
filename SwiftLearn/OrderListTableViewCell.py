import UIKit

class OrderListTableViewCell: UITableViewCell {
	
	//充值日
	@IBOutlet weak var dateLabel: UILabel!
	//充值时
	@IBOutlet weak var hourLabel: UILabel!
	//充值金额
	@IBOutlet weak var moneyLabel: UIlabel!
	//充值月数
	@IBOutlet weak var monthLabel: UILabel!
	//支付状态
	@IBOutlet weak var statusLabel: UILabel!

	override func awakeFromNib() {
		super.awakeFromNib()
	}

	override func setSelected(_ selected: Bool, animated: Bool) {
		super.setSelected(selected, animated: animated)
	}
}