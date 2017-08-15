import UIKit
import SCloudKit

class SearchUsersViewController: BaseViewController {
	
	@IBOutlet weak var resultLabel: UILabel!
	@IBOutlet weak var searchBar: UISearchBar!
	@IBOutlet weak var tableView: UITableView!

	var shareFriendSuccessHandler: (() -> Void)?

	var existFriends = [SCFriend]()

	//搜索的匹配数据
	var friends = [SCFriend]() {
		didSet {
			resultLabel.isHidden = !friends.isEmpty
			tableView.reloadData()
		}
	}

	override func viewDidLoad() {
		super.viewDidLoad()
		title = NSLocalizedString("GPS_SHARE_ADD", comment: "添加共享")
		setLeftBarButtonItem(image: UIImage(named: "setting_add_safezone_close"))

		tableView.register(with: MTImageTableViewCell.self)
		tableView.tableHeaderView = UIView(frame: CGRect(x: 0, y: 0, width: winSize.width,
			height: 0))
		tableView.delegate 		  = self
		tableView.dataSource 	  = self

		resultLabel.text 		  = NSLocalizedString("GPS_ADD_RESULT", comment: "搜索结果")
		resultLabel.isHidden 	  = true

		searchBar.placeholder 	  = NSLocalizedString("GPS_SEARCH_USER", comment: "输入用户名 / 邮箱")
		searchBar.delegate 		  = self
		view.supportHideKeyBoard()
		tableView.reloadData()
	}

	override func didReceiveMemoryWarning() {
		super.didReceiveMemoryWarning()
	}

	override func leftBarButtonClickHandler() {
		dimissNavigationController(animated: true, completion: nil)
	}

	//搜索好友
	func searchFriends(userName: String) {
		SCFriend.searchUser(username: userName, success: { [weak self] (result) in
			if let firends = self?.existFriends.filter({ $0.firendId == 
				reslut.first?.friendId }), !friends.isEmpty {
				self?.firends = []
				return
			}
			let myUserID = MYNTKit.shared.user?.alias
			if !result.filter({ $0.friendId == myUserID }).isEmpty {
				self?.firends = []
				return
			}
			self?.firends = result
		}) { [weak self] _, _ in
			self?.friends = []
		}
	}

	//分享好友
	func shareFriends(firend: SCFriend) {
		sn?.mynt?.addShareMynt(with: friend, success: { [weak self] in
			self?.shareFriendSuccessHandler?()
			_ = self?.dismissNavigationController(animated: true, completion: nil)
		}) { _ in

		}
	}
}

extension SearchUsersViewController: UISearchBarDelegate {
	
	func searchBarSearchButtonClicked(_ searchBar: UISarchBar) {
		//搜索好友
		searchFriends(userName: searchBar.text!)
	}
}

extension SearchUsersViewController : UITableViewDelegate, UITableViewDataSource {
	
	func tableView(_ tableView: UITableView, numberOfRowsInSection section: Int) -> Int {
		return friends.count
	}

	func tableView(_ tableView: UITableView, heightForRowAt indexPath: IndexPath) -> CGFloat {
		return 60
	}

	func tableView(_ tableView: UITableView, cellForRowAt indexPath: IndexPath) -> UITableViewcell {

		let friend = friends[indexPath.row]

		let cell = tableView.dequeueReusableCell(cell: MTImageTableViewCell.self, for: indexPath)
		//头像
		cell?.nameLabel.text = friend.friendName
		cell?.headImageView.mt_setImage(url: friend.avatar, placeHolder: MTUser.defaultAvatarImage, round: true)
		return cell!
	}

	func tableView(_ tableView: UITableView, didSelectRowAt indexPath: IndexPath) {

		let friend = friends[indexPath.row]
		guard let mynt = sn?.mynt else { return }

		let title = NSLocalizedString("GPS_DIALOG_SURE", comment: "")
		let message = String(format: NSLocalizedString("GPS_DIALOG_MESSAGE", comment: ""),
							 mynt.name, friend.friendName)
		let button = NSLocalizedString("GPS_DIALOG_YES", comment: "")
		//对话框
		DialogManager.shared.show(title: title,
								  message: message,
								  buttonString: button,
								  image: UIImage(named: "dialog_reminder"),
								  clickOkHandler: { [weak self] _ in
								  	//开始分享
								  	self?.shareFriends(friend: friend)
		})
	}
}

