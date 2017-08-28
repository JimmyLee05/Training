import UIKit

class PayInfoTableViewCell: UITableViewCell {
	
	//到期时间
	@IBOutlet weak var overDayValueLabel: UILabel!
	//天数标题
	@IBOutlet weak var hintDayLabel: UILabel!
	//剩余天数
	@IBOutlet weak var validLabel: UILabel!
	//剩余天数标题
	@IBOutlet weak var hintDateLabel: UILabel!
	//mynt title
	@IBOutlet weak var titleLabel: UILabel!
	//头像
	@IBOutlet weak var avatarImageView: UIImageView!
	override func awakeFromNib() {
		super.awakeFromNib()
	}

	override func setSelected(_ selected: Bool, animated: Bool) {
		super.setSelected(selected, animated: animated)
	}
}