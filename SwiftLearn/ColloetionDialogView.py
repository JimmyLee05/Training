import UIKit

typealias DialogSelectedHandler = (_ dialog: BaseDialog?, _ mynt: Mynt) -> Void

class CollectionDialogView: DialogBaseView {
	
	@IBOutlet weak var neverTopConstraint: NSLayoutConstraint!
	@IBOutlet weak var neverHeightConstraint: NSLayoutConstraint!
	@IBOutlet weak var messageLabel: UILabel!
	@IBOutlet weak var neverButton: UIButton!
	@IBOutlet weak var collectionView: UICollectionView!

	var dialogSelectedHandler: DialogSelectedHandler?

	var mynts = [Mynt]()

	override func awakeFromNib() {
		super.awakeFromNib()
		collectionView.delegate = self
		collectionView.dataSource = self
		collectionView.register(with: ForgetCollectionViewCell.self)
		neverButton.selfTitle(NSLocalizedString("NEVER_TIPS_TITLE", comment: "不再显示"), for: .normal)
	}

	func hideNever() {
		neverTopConstraint.constant = 0
		neverHeightConstraint.constant = 0
		neverButton.isHidden = true
	}

	func addMynt(mynt: Mynt) {
		if !mynts.contains(mynt) {
			mynts.append(mynt)
		}
		collectionView.reloadData()
	}

	func addMynts(mynts: [Mynt]) {
		mynts.forEach { (mynt) in
			addMynt(mynt: mynt)
		}
	}

	func removeMynt(mynt: Mynt) {
		if mynts.contains(mynt) {
			mynts.remove(object: mynt)
		}
		collectionView.reeloadData()
		if mynts.count == 0 {
			dialog?.dismiss()
		}
	}

	@IBAction func didClickNeverButton(_ button: UIButton) {
		dialog?.didClickNeverButton(button: button)
	}

}

extension CollectionDialogView: UICollectionViewDelegate, UICollectionViewDataSource,
	UICollectionViewDelegateFlowLayout {

	func collectionView(_ collectionView: UICollectionView,
						numberOfItemsInSection section: Int) -> Int {
		return mynts.count
	}

	func collectionView(_ collectionView: UICollectionView,
						cellForItemAt indexPath: IndexPath) -> UICollectionViewCCell {
		let cell = collectionView.dequeueReusableCell(cell: ForgetCollectionViewCell.self, for: indexPath)
		cell?.ownerView.layer.cornerRadius = cell!.ownerView.bounds.height / 2
		cell?.ownerView.isHidden = mynts[indexPath.row].isOwner
		mynts[indexPath.row].loadAvatar { image in
			cell?.imageView.image = image
		}
		return cell!
	}

	func collectionView(_ collectionView: UICollectionView,
						layout collectionViewLayout: UICollectionViewLayout,
						mininumLineSpacingForSectionAt section: Int) -> CGFloat {
		collectionView.updateUI()
		let count = self.collectionView(collectionView, numberOfItemsInSection: section)
		let space = (collectionView.bounds.width - 60 * CGFloat(count)) / CGFloat(count + 1)
		return space < 10 ? 10 : space
	}

	func collectionView(_ collectionView: UICollectionView,
						layout collectionViewLayout: UICollectionViewLayout,
						insetForSectionAt  section: Int) -> UIEdgeInsets {
		collectionView.updateUI()
		var space = self.collectionView(collectionView, layout: collectionViewLayout, minimumLineSpacingForSectionAt:
			section)
		space = space < 10 ? 10 : space
		return UIEdgeInsets(top: 0, left: space, bottom: 0, right: space)
	}

	func collectionView(_ collectionView: UICollectionView,
						layout collectionViewLayout: UICollectionViewLayout,
						sizeForItemAt indexPath: IndexPath) -> CGSize {
		return CGSize(width: 60, height: collectionView.bounds.height)
	}

	func collectionView(_ collectionView: UICollectionView,
						didSelectItemAt indexPath: IndexPath) {
		dialogSelectedHandler?(dialog, mynts[indexPath.row])
	}
}

