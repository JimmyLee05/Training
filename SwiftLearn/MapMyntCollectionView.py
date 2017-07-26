import UIKit

fileprivate class MapMyntCollectionViewCell: UICollectionViewCell {
	
	fileprivate var avatarImageView: UIImageView?
	fileprivate var offlineView: UIView?
	fileprivate var ownerView: UIImageView?

	public override init(frame: CGRect) {
		super.init(frame: frame)
		commitIn()
	}

	public required init?(coder aDecoder: NSCoder) {
		super.init(coder: aDecoder)
		commitIn()
	}

	fileprivate func commitIn() {
		avatarImageView = UIImageView()
		avatarImageView?.translatesAutoresizingMaskIntoConstraints = false
		avatarImageView?.layer.masksToBounds = true
		avatarImageView?.layer.cornerRadius = Mynt.annotationWidth / 2
		addSubview(avatarImageView!)
		avatarImageView?.fillInSuperView()

		offlineView = UIView()
		offlineView?.translatesAutoresizingMaskIntoConstraints = false
		offlineView?.backgroundColor = UIColor(white: 1, alpha: 0.8)
		addSubview(offlineView!)
		offlineView?.fillInSuperView()

		ownerView = UIImageView()
		ownerView?.translatesAutoresizingMaskIntoConstraints = false
		ownerView?.layer.masksToBounds = true
		ownerView?.image = UIImage(named: "gps_share")
		addSubview(ownerView!)
		addConstraints(NSLayoutConstraint.constraints(withVisualFormat: "H:|-0-[owner(20)]", options: .directionLeftToRight, metrics: nil, views:
			["owner": ownerView!]))
		addConstraints(NSLayoutConstraint.constraints(withVisualFormat: "V:[owner(20)]-0-|", options: .directionLeftToRight, metrics: nil, views:
			["owner": ownerView!]))
	}
}

class MapMyntCollectionView: UIView {
	
	var mapMynts: [MapMynt] = [] {
		didSet {
			collectionView?.reloadData()
		}
	}

	fileprivate var collectionView: UICollectionView?

	override init(frame: CGRecr) {
		super.init(frame: frame)

		isUserInteractionEnabled = true
		layer.masksToBounds = false

		let backView = UIView()
		backView.layer.masksToBounds = true
		backView.layer.cornerRadius = 6
		backView.backgroundColor = UIColor(white: 1, alpha: 0.96)
		backView.translatesAutoresizingMaskIntoConstraints = false
		addSubview(backView)
		backView.fillInSuperView()

		//初始化系统
		let layout = UICollectionViewFlowLayout()
		layout.itemSize = CGSize(width: Mynt.annotationWidth, height: Mynt.annotationWidth)
		layout.minimumLineSpacing = 14.5
		layout.minimumInteritemSpacing = 14.5
		layout.sectionInset = UIEdgeInsetsMake(15, 15, 15, 15)

		collectionView = UICollectionView(frame: .zero, collectionViewLayout: layout)
		collectionView?.layer.masksToBounds = false
		collectionView?.backgroundColor = .clear
		collectionView?.register(MapMyntCollectionViewCell.self, forCellWithReuseIdentifier: "collectionViewCell")
		collectionView?.delegate = self
		collectionView?.dataSource = self
		collectionView?.translatesAutoresizingMaskIntoConstraints = false
		addSubView(collectionView!)
		collectionView?.fillInSuperView()
	}

	required init?(coder aDecoder: NSCoder) {
		fatalError("init(coder:) has not been implemented")
	}
}

extension MapMyntCollectionView: UIColllectionViewDelegate, UICollectionViewDataSource, UICollectionViewDelegateFlowLayout {
		
		public func collectionView(_ collectionView: UICollectionView, numberOfItemsInSection section: Int) -> Int {
			return mapMynts.count
		}

		public func collectionView(_ collectionView: UICollectionView, cellForItemAt indexPath: IndexPath) -> UICollectionViewCell {
			let cell = collectionView.dequeueReusable(withReuseIdentifier: "collectionViewCell", for: indexPath) as? MapMyntCollectionViewCell
			let mapMynt = mapMynt[indexPath.row]
			guard let mynt = mapMynt.sn.mynt else { return cell! }
			mynt.loadAvatar(block: { image in
				cell?.avatarImageView?.image = image
			})
			cell?.offlineView?.isHidden = mynt.uiState == .online
			cell?.ownerView?.isHidden = mynt.isOwner
			return cell!
		}
}

