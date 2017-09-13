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
			result.isHidden = !friends.isEmpty
			tableView.reloadData()
		}
	}

	override func viewDidLoad() {
		super.viewDidLoad()
		title = MTLocalizedString("GPS_SHARE_ADD", comment: "添加共享")
		setLeftBarButtonItem(image: Resource.Image.Navigation.close)

		tableView.register(with: MTImageTableViewCell.self)
		tableView.tableHeaderView = UIView(frame: CGRect(x: 0, y: 0, width: winSize.width, height: 0))
		tableView.delegate 		= self
		tableView.dataSource 	= self

		resultLable.text 		= MTLocalizedString("GPS_ADD_RESULT", comment: "搜索结果")
		resultLabel.isHidden 	= true

		searchBar.placeholder 	= MTLocalizedString("GPS_SEARCH_USER", comment: "输入用户名 ／ 邮箱")
		searchBar.delegate 		= self
		view.supportHideKeyBoard()
		tableView.reloadData()
	}

	override func didReceiveMemoryWarning() {
		super.didReceiveMemoryWarning()
	}

	override func leftBarButtonClickedHandler() {
		dismissNavigationController(animated: true, completion: nil)
	}

	//搜索好友
	func searchFriends(userName: String) {
		SCFriend.searchUser(username: userName, success: { [weak self] (result) in
			if let friends = self?.existFriends.filter({ $0.friendId == result.firendId }), !friend.isEmpty {
				self?.friend = []
				return
			}
			let userId = MYNTKit.shared.user?.userId
			if !result.filter({ $0.friendId == userId }).isEmpty {
				self?.friends = []
				return
			}
			self?.friends = result
		}) { [weak self] _, _ in
			self?.friends = []
		}
	}
	//分享好友
	func shareFriends(friend: SCFriend) {
		mynt?.share(userId: friend.friendId, success: { [weak self] in
			self?.shareFriendSuccessHandler?()
			_ = self?.dismissNavigationController(animated: true, completion: nil)
		}) { _ in

		}
	}
}

extension SearchUsersViewController: UISearchBarDelegate {
	
	func searchBarSearchButtonClicked(_ searchBar: UISearchBar) {
		//搜索好友
		searchFriends(userName: searchBar.text!)
	}
}

extension SearchUsersViewController: UITableViewDelegate, UITableViewDataSource {
	
	func tableView(_ tableView: UITableView, numberOfRowsInSection section: Int) -> Int {
		return friends.count
	}

	func tableView(_ tableView: UITableView, heightForRowAt indexPath: IndexPath) -> UITableViewCell {
		return 60
	}

	func tableView(_ tableView: UITableView, cellForRowAt indexPath: IndexPath) -> UITableViewCell {

		let friend = friend[indexPath.row]
		let cell = tableView.dequeueReusableCell(cell: MTImageTableViewCell.self, for: indexPath)
		//头像
		cell?.nameLabel.text = friend.friendName
		MKImageCache.shared.downUserAvatar(url: friend.avatar) { image in
			cell?.headImageView.image = image?.round()
		}
		return cell!
	}

	func tableView(_ tableView: UITableView, didSelectRowAt indexPath: IndexPath) {

		let friend = friends[indexPath.row]
		guard let mynt = mynt else { return }

		let title 		= MTLocalizedString("GPS_DIALOG_SURE", comment: "")
		let message		= MTLocalizedString("GPS_DIALOG_MESSAGE", comment: "")
		let button 		= MTLocalizedString("GPS_DIALOG_YES", comment: "")

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


