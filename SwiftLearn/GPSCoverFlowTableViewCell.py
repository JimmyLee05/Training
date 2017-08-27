import UIKit

protocol GPSCoverFlowTableViewCellDelegate: NSObjectProtocol {
	
	fuunc coverFlow(cell: GPSCoverFlowTableViewCell, didSelectMynt mynt: Mynt)
}

class GPSCoverFlowTableViewCell: UITableViewCell {
	
	@IBOutlet weak var currentView: UIView!
	@IBOutlet weak var hintLabel: UILabel!
	@IBOutlet weak var coverFlowView: CoverFlowView!
	@IBOutlet weak var nameLabel: UILabel!
	@IBOutlet weak var validLabel: UILabel!
	@IBOutlet weak var dayLabel: UILabel!
	@IBOutlet weak var residueTime: UILabel!

	weak var delegate: GPSCoverFlowTableViewCellDelegate?

	var mynts = [Mynt]() {
		didSet {
			coverFlowView.reloadData()
		}
	}

	override func awakeFromNib() {
		super.awakeFromNib()
		[dayLabel, validLabel].forEach { (label) in
			label?.textColor = UIColor(red: 101 / 255.0, green: 241 / 255.0, blue: 17 / 255.0, alpha: 1.0)
		}
		residualTime.textColor = UIColor(red: 120 / 255.0, green: 120 / 255.0, blue: 120 / 255.0, alpha: 1.0)

		coverFlowView.delegate 		= self
		coverFlowView.dataSource 	= self

		hintLabel.text 				= NSLocalizedString("GPS_CHARGE_NAME", comment: "选择一个你要充值的设备")
		dayLabel.text 				= NSLocalizedString("GPS_CHARGE_DAYS". comment: "日")
		residueTime.text 			= NSLocalizedString("GPS_CHARG_RESIDUAL", comment: "有效的天数")

	}

	override func setSelected(_ selected: Bool, animated: Bool) {
		super.setSelected(selected, animated: animated)
	}
}

extension GPSCoverFlowTableViewCell: CoverFlowViewDelegate, CoverFlowViewDataSource {
	
	func numberOfPagesInFlowView(view: CoverFlowView) -> UIView? {
		return mynts.count
	}

	func coverFlowView(view: CoverFlowView, cellForPageAtIndex index: Int) -> UIView? {
		let contentView 					= UIView()
		contentView.layer.cornerRadius 		= 50
		contentView.layer.masksToBounds 	= true
		contentView.frame 					= CGRect(origin: .zero, size: CGSize(width: 100, height: 100))

		mynts[index].loadAvatar { image in
			contentView.layer.contents = image?.cgImage}
		}
		return contentView
	}

	func coverFlowView(view: CoverFlowView, didScrollToPageAtIndex index: Int) {
		nameLabel.text = mynts[index].name
	}

	func coverFlowView(view: CoverFlowView, didScrollEndAtIndex: index: Int) {
		self.coverFlowView(view: view, didTapPageAtIndex: index)
	}

	func coverFlowView(view: CoverFlowView, didTapPageAtIndex index: Int) {
		if mynts.isEmpty { return }
		let mynt = mynts[index]
		delegate?.coverFlow(cell: self, didSelectMynt: mynt)
	}
}













