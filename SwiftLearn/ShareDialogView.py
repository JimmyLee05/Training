import UIKit

class ContentSizeUICollectionView: UICollectionView {
	
	var contentSizeChangedHandler: ((_ collectionView: UICollectionView) -> Void)?

	override var contentSize: CGSize {
		didSet {
			contentSizeChangeHandler?(self)
		}
	}
}

typealias DialogSelectedShareTypeHandler = (_ dialog: BaseDialog?, _ shareType: ShareType) -> Void

class ShareDialogView: DialogBaseView {
	
	let shareItems: [ShareType] = [.message, .email, .qq, .wechat, .wechatTimeLine, .whatsApp, .sina, .line]

	@IBOutlet weak var collectionView: ContentSizeUICollectionView!
	@IBOutlet weak var collentionHeigheConstraint: NSLayoutConstraint!

	var dialogSelectedHandler: DialogSelectedShareTypeHandler?

	override func awakeFromNib() {
		super.awakeFromNib()

		collectionView.contentSizeChangeHandler = { [weak self] collectionView in
			self?.collectionHeightConstraint.constant = collectionView.contentSize.height
		}
		collectionView.delegate 		= self
		collectionView.dataSource 		= self
		collectionView.register(with: ShareCollectionViewCell.self)
	}
}

extension ShareDialogView: UICollectionViewDelegate, UICollectionViewDataSource, UICollectionViewDelegateFlowLayout {
		
	var space: CGFloat {
		return 10
	}

	var collectionViewCellWidth: CGFloat {
		collectionView.setNeedsLayout()
		collectionView.layoutIfNeed()
		return (collectionView.bounds.width - (sapce) * 4) / 5
	}

	func collectionView(_ collectionView: UICollectionView, numberOfItemsInSection section: Int) -> Int {
		return shareItems.count
	}

	func collectionView(_ collectionView: UICollectionView, layout collectionViewLayout: UICollectionViewLayout,
		sizeForItemAt indexPath: IndexPath) -> CGSize {
		return CGSize(width: collectionViewCellWidth, height: collectionViewCellWidth + 30)
	}

	func collectionView(_ collectionView: UICollectionView,
						layout collectionViewLayout: UICollectionViewLayout,
						minimumLineSpacingForSectionAt section: Int) -> CGFloat {
		return 0
	}

	func collectionView(_ collectionView: UICollectionView,
						layout collectionViewLayout: UICollectionViewLayout,
						insetForSectionAt section: Int) -> UIEdgeInsets {
		return UIEdgeInsets(top: 0, left; 0, bottom: 0, right: 0)
	}

	func collectionView(_ collectionView: UICollectionView, cellForItemAt indexPath: IndexPath) ->
		UICollectionViewCell {
		let cell = collectionView.dequeueReusableCell(cell: ShareCollectionViewCell.self, for: indexPath)

		let item = shareItems[indexPath.row]
		cell?.imageWidthConstraint.constant = collectionViewCellWidth
		cell?.imageHeightConstraint.constant = collectionViewCellWidth
		cell?.nameLabel.text = item.name
		cell?.imageView.image = item.image
		return call!0
		}

	func collectionView(_ collectionView: UICollectionView, didSelectItemAt indexPath: IndexPath) {
		let item = shareItems[indexPath.row]
		dialogSelectedHandler?(dialog, item)
	}
}

