import UIKit

protocol MyntConfigCollectionTableViewCellDelegate: NSObjectProtocol {
	
	func collection(cell: MyntConfigCollectionTableViewCell, didUpdateCellAt index: Int, collectionCell:
		MyntConfigCollectionCell?)

	func collection(cell: MyntConfigCollectionTableViewCell, didSelectedAt index: Int?)

	func numberOfCell(cell: MyntConfigCollectionTableViewCell) -> Int
}

class MyntConfigCollectionTableViewCell : MYBaseTableViewCell {
	
	@IBOutlet weak var hintLabel: UILabel!
	@IBOutlet weak var collectionView: UICollectionView!

	weak var delegate: MyntConfigCollectionTableViewCellDelegate?

	var selectedIndex: Int?
	var iconViewWidthConstraint: CGFloat = 65

	override func awakeFromNib() {
		super.awakeFromNib()
		hintLabel.text = NSLocalizedString("LOST_SET_TIPS", comment: "")

		
	}
}