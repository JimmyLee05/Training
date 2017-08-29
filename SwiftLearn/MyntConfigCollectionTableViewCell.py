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

		collectionView.register(with: MyntConfigCollectionCell.self)
		collectionView.delegate 	= self
		collectionView.dataSource 	= self
	}
}

// MARK: - UICollectionViewDataSource, UICollectionViewDelegateFlowLayout
extension MyntConfigCollectionTableViewCell: UICollectionViewDataSource, UICollectionViewDelegateFlowLayout,
	UICollectionViewDelegate {

	func collectionView(_ collectionView: UICollectionView,
						numberOfItemsInSection section: Int) -> Int {
		if let count = delegate?.numberOfCell(cell: self) {
			return count
		}
		return 0
	}

	//数据源
	func collectionView(_ collectionView: UICollectionView,
						cellForItemAt indexPath: IndexPath) -> UICollectionViewCell {
		let cell = collectionView.dequeueReusableCell(cell: MyntConfigCollectionCell.self, for: indexPath)
		delegate?.collection(cell: self, didUpdateCellAt: indexPath.row, collectionCell: cell)
		return cell!
	}

	func collectionView(_ collectionView: UICollectionView,
						cellForItemAt indexPath: IndexPath) -> UICollectionViewCell {
		let cell = collectionView.dequeueReusableCell(cell: MyntConfigCollectionCell.self, for: indexPath)
		delegate?.collection(cell: self, didUpdateCellAt: indexPath.row, collectionCell: cell)
		return cell!
	}

	func collectionView(_ collectionView: UICollectionView,
						layout collectionViewLayout: UICollectionViewLayout,
						insetForSectionAt section: Int) -> UIEdgeInsets {
		let count = self.collectionView(collectionView, numberOfItemsInSection: section)
		let space = (winSize.width - iconViewWidthConstraint * CGFloat(count)) / CGFloat(count + 1)
		return space
	}

	func collectionView(_ collectionView: UICollectionView,
						layout collectionViewLayout: UICollectionViewLayout,
						sizeForItemAt indexPath: IndexPath) -> CGSize {
		return CGSize(width: iconViewWidthConstraint, height: collectionView.bounds.height)
	}

	//点击事件
	func collectionView(_ collectionView: UICollectionView,
						didSelectItemAt indexPath: IndexPath) {
		let cell = collectionView.cellForItem(at: indexPath) as? MyntConfigCollectionCell
		if cell?.state == .disable { return }
		self.selectedIndex = self.selectedIndex == indexPath.row ? nil : indexPath.row
		delegate?.collection(cell: self, didSelectedAt: selectedIndex)
		collectionView.reloadData()
	}
}


