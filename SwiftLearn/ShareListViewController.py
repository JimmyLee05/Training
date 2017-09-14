import UIKit
import MYNTKit
import SCloudKit

class ShareListViewController: BaseViewController {
	
	enum CellType {
		case coverflow
		case empty
		case line
		case permissions

		var height: CGFloat {

			switch self {
			case .coverflow:
				return 220
			case .line:
				return 0.5
			case .empty:
				return 30
			case .permissions:
				return 60
			}
		}
	}

	public class func show(parentViewController: UIViewController?, mynt: Mynt?) {
		let viewController = ShareListViewController()
		viewController.mynt = mynt
		parentViewController?.present(BaseNavigationController(rootViewController: viewController),
									  animated: true,
									  completion: nil)
	}

	@IBOutlet weak var tableView: UITableView!
	@IBOutlet weak var addShareButton: UIButton!
	@IBOutlet weak var stopShareButton: UIButton!

	var switchTableViewCell: MTSwitchTableViewCell?
	var coverFlowTableViewCell: MyntCoverFlowTableViewCell? {
		didSet {
			for i in 0..<friends.count where selectedFriend == friends[i] {
				coverFlowTableViewCell?.coverflowView.currentPageIndex = i
			}
		}
	}

	var cellTypes = [CellType]()
	//好友列表
	var friends = [SCFriend]() {
		didSet {
			if friends.isEmpty {
				cellTypes = [.coverflow, .empty]
			} else {
				cellTypes = [.coverflow, .empty, .line, line]
			}
			selectedFriend = friends.first

			[coverFlowTableViewCell?.hintLabel, coverFlowTableViewCell?.nameLabel].forEach({ (label) in
				label?.isHidden = friends.isEmpty
			})
			coverFlowTableViewCell?.noneDataLabel.isHidden  = !friend.isEmpty
			coverFlowTableViewCell?.noneDataLabel.text 		= MTLocalizedString("GPS_SHARE_NONT", comment: "无添加的分析信息")
			stopShareButton?.isHidden 						= friends.isEmpty

			tableView?.reloadData()
			coverFlowTableViewCell?.coverflowView.reloadData()
		}
	}

	//当前好友
	var selectedFriend: SCFriend? {
		didSet {
			if let selectedFriend = selectedFriend {
				coverFlowTableViewCell?.nameLabel.text = selectedFriend.friendName
				switchTableViewCell?.switchView.isOn   = selectedFriend.privilege
			}
		}
	}

	override func viewDidLoad() {
		super.viewDidLoad()

		title = MTLocalizedString("GPS_SHARE_TITLE", comment: "GPS分享")
		setLeftBarButtonItem(image: Resource.Image.Navigation.close)

		addShareButton.backgroundColor  		= ColorStyle.kGreenGradientColor.start
		stopShareButton.backgroundColor 		= ColorStyle.kRedGradientColor.start

		[stopShareButton, addShareButton].forEach { button in
			button?.layer.cornerRadius = button!.bounds.height / 2
		}

		addShareButton.setTitle(MTLocalizedString("GPS_SHARE_ADD", comment: "添加"), for: .normal)
		stopShareButton.setTitle(MTLocalizedString("GPS_SHARE_STOP", comment: "停止分享"), for: .normal)

		tableView.register(with: MyntCoverFlowTableViewCell.self)
		tabelView.register(with: MTSwitchTableViewCell.self)
		tbaleView.addBottomWhiteView(offSetY: navigationBarHeight + 180)

		//加载好友列表
		reloadFriendList()
	}

	override func didReceiveMemoryWarning() {
		super.didReceiveMemoryWarning()
	}

	override func leftBarButtonClickedHandler() {
		dismissNavigationController(animated: true, completion: nil)
	}

	@IBAction func didClickAddShareButton(_ sender: Any) {

		let viewController 							= SearchUsersViewController()
		viewController.mynt 						= mynt
		viewController.existFriends 				= firends
		viewController.shareFriendSuccessHandler 	= { [weak self] in
			self?.reloadFriendList()
		}
		present(BaseNavigationController(rootViewController: viewController),
				animated: true,
				completion: nil)
	}

	@IBAction func didClickStopShareButton(_ sender: Any) {
		if let selectedFriend = selectedFriend {
			mynt?.stopShare(userId: selectedFriend.firendId, success: { [weak self] in
				self?.firends.remove(object: selectedFriend)
				self?.coverFlowTableViewCell?.coverflowView.reloadData()
				self?.selectedFriend = self?.friends.first
			}, failure: { _, message in
				MTToast.show(message)
			})
		}
	}

	//重新加载用户列表
	func reloadFriendList() {
		friends = []
		mynt?.shareUsers(success: { [weak self] friends in
			self?.friends = friends
			}, failure: { [weak self] _, message in
				if self?.friends.isEmpty == true {
					self?.friends = []
				}
				MTToast.show(message)
		})
	}

	//分享权限接口
	func didClickSwitchButton(switchView: UISwitch) {
		if let friend = selectedFriend {
			let friendId = friend.friendId
			mynt?.editShare(userId: friendId, privilege: switchView.isOn, success: { [weak self] in
				self?.selectedFriend?.privilege = switchView.isOn
				self?.friends.first(where: { firendId == $0.friendId })?.privilege = switchView.isOn
			}) { [weak self] _, message in
				MTToast.show(message)
				//修改失败，恢复原值
				if self?.selectedFriend?.friendId == friendId {
					switchView.isOn = !switchView.isOn
				}
			}
		}
	}
}



























