import UIKit
import SCloudKit

class SearchUsersViewController: BaseViewController {
	
	@IBOutlet weak var resultLabel: UILable!
	@IBOutlet weak var searchBar: UISearchBar!
	@IBOutlet weak var tableView: UITableView!

	var shareFriendSuccessHandler: (() -> Void)?

	var existFriends = [SCFriend]()
	// 搜索的匹配数据
	var friends = [SCFriend]() {
		didSet {
			resultLabel.isHidden = !friends.isEmpty
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

		resultLabel.text 		= MTLocalizedString("GPS_ADD_RESULT", comment: "搜索结果")
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

	// 搜索好友
	func searchFriends(userName: String) {

		SCFriend.searchUser(username: userName, success: { [weak self] (result) in
			if let friends = self?.existFriends.filter({ $0.friendId == result.first?.friendId }), !friends.isEmpty {
				self?.friends = []
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

	// 分享好友
	func shareFriends(friend: SCFriend) {
		mynt?.share(userId: friend.friendId, success: { [weak self] in
			self?.shareFriendSuccessHandler?()
			_ = self?.dismissNavigationController(animated: true, completion: nil)
		}) { _ in

		}
	}

}

extension SearchUsersViewController : UISearchBarDelegate {
	
	func searchBarSearchButtonClicked(_ searchBar: UISearchBar) {
		//搜索好友
		searchFriends(userName: searchBar.text!)
	}
}

extension SearchUsersViewController: UITableViewDelegate, UITableViewDataSource {
	
	func tableView(_ tableView: UITableVIew, numberOfRowsInSection section: Int) -> Int {
		return friend
	}
}


























