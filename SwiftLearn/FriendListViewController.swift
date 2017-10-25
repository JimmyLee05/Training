//
//  FriendListViewController.swift
//  Slife
//
//  Created by 李南君 on 2017/10/24.
//  Copyright © 2017年 Slightech. All rights reserved.
//

import UIKit

//初始化主界面
class FriendListViewController: UIViewController,NSFetchedResultsControllerDelegate {
    
    
    @IBOutlet weak var tableView: UITableView!
    @IBOutlet weak var labelNoSouSuo: UILabel!
    @IBOutlet weak var theSearchBar: UISearchBar!
    
    var indexArray: NSMutableArray?
    var letterResultArr: NSMutableArray?
    
    var addFriendNotice: UILabel?
    var addFriendButton: UIButton?
    var recommondButton: UIButton?
    var noticeView: UIView?
    var fetchedResultsController: NSFetchedResultsController<NSFetchRequestResult>?

    var searchTextField: UITextField?
    
    var listFriends = [Friend]()
    var groupFriends = [[Friend]]()
    
    override func viewDidLoad() {
        
        super.viewDidLoad()
        self.view.backgroundColor = UIColor.white
        self.navigationController?.navigationBar.barStyle = .default
        view.supportHideKeyBoard()
        
        initNavigationBar()
        reloadData()
        getFetchedResultsController()
        initSearchBarView()
        initlabelNoSouSuo()
        initTableView()
        filterContentForSearchBarText("")
    }
    
    override func viewWillAppear(_ animated: Bool) {
        super.viewWillAppear(animated)
        self.navigationController?.navigationBar.lt_reset()
        refreshNotice()
        if STStorage.sharedInstance().countFriends() > 0 {
            noticeView?.isHidden = true
        } else {
            noticeView?.isHidden = false
        }
    }
    
    override func viewWillDisappear(_ animated: Bool) {
        super.viewWillDisappear(animated)
        self.view.endEditing(true)
    }
    
    override var preferredStatusBarStyle: UIStatusBarStyle {
        return UIStatusBarStyle.default
    }
    
    override func didReceiveMemoryWarning() {
        super.didReceiveMemoryWarning()
    }
}


//初始化子控件，定义导航栏和搜索栏的相关属性
extension FriendListViewController: UISearchBarDelegate ,UISearchDisplayDelegate {
    
    private func initNavigationBar() {
        let titleLabel = UILabel.init(frame: CGRect(x: 0, y: 0, width: SCREEN_WIDTH, height: 20))
        titleLabel.textColor = UIColor(red: 74 / 255.0, green: 74 / 255.0, blue: 74 / 255.0, alpha: 1.0)
        titleLabel.textAlignment = NSTextAlignment.center
        titleLabel.font = UIFont.createWithFontSize(15.0)
        titleLabel.text = "FRIENDS".local()
        
        self.navigationItem.titleView = titleLabel
        self.navigationItem.leftBarButtonItem = UIBarButtonItem(image: UIImage(named: "home_menu_black"), style: UIBarButtonItemStyle.plain, target: self, action: #selector(homeMenu))
        self.navigationItem.leftBarButtonItem?.tintColor = MAIN_TEXT_COLOR
        self.navigationItem.rightBarButtonItem = UIBarButtonItem(image: UIImage(named: "friend_add"), style: UIBarButtonItemStyle.plain, target: self, action: #selector(addFriend))
        
        self.navigationItem.rightBarButtonItem?.tintColor = MAIN_TEXT_COLOR
        refreshNotice()
        self.navigationController?.navigationBar.lt_setBackgroundColor(UIColor.white)
    }
    
    private func initlabelNoSouSuo() {
        
        labelNoSouSuo.text              = "FRIEND_SEARCH_NONE".local()
        labelNoSouSuo.isHidden          = true
    }
    
    private func initSearchBarView() {
        
        theSearchBar.autocapitalizationType     = UITextAutocapitalizationType.allCharacters
        theSearchBar.autocorrectionType         = UITextAutocorrectionType.no
        theSearchBar.keyboardType               = UIKeyboardType.emailAddress
        theSearchBar.placeholder                = "FRIEND_SEARCH_HINT".local()
    }
}

extension UIView {
    
    @objc public func supportHideKeyBoard() {
        let tapGestureRecognizer = UITapGestureRecognizer(target: self, action: #selector(UIView._keyboardHide))
        tapGestureRecognizer.cancelsTouchesInView = false
        self.addGestureRecognizer(tapGestureRecognizer)
    }
    
    @objc fileprivate func _keyboardHide() {
        _resignFirstResponder(self)
    }
    
    fileprivate func _resignFirstResponder(_ view: UIView) {
        for v in view.subviews {
            if v.isFirstResponder {
                v.resignFirstResponder()
                return
            } else {
                _resignFirstResponder(v)
            }
        }
    }
}


//初始化UITableView
extension  FriendListViewController: UITableViewDataSource , UITableViewDelegate {
    
    private func initTableView() {

        tableView.dataSource = self
        tableView.delegate = self
        tableView.tableFooterView = UIView()
    }
    
    func tableView(_ tableView: UITableView, cellForRowAt indexPath: IndexPath) -> UITableViewCell {
        
        let friend = groupFriends[indexPath.section][indexPath.row]
        
        var cell = tableView.dequeueReusableCell(withIdentifier: "STFriendViewCell") as? STFriendViewCell
        if cell == nil {
            cell = STFriendViewCell(style: UITableViewCellStyle.default, reuseIdentifier: "STFriendViewCell")
        }
        cell!.setFriend(user: friend)
        
        return cell!
    }
    
    func tableView(_ tableView: UITableView, heightForRowAt indexPath: IndexPath) -> CGFloat {
        return 55
    }
    
    func numberOfSectionsInTableView(tableView: UITableView) -> Int {
        if indexArray == nil {
            return 0
        }
        return (indexArray?.count)!
    }
    
    func tableView(_ tableView: UITableView, numberOfRowsInSection section: Int) -> Int {
        if letterResultArr == nil{
            return 0
        }
        return ((letterResultArr?.object(at: section) as AnyObject).count)!
    }
    
    func sectionIndexTitlesForTableView(tableView: UITableView) -> [String]? {
        if (indexArray == nil) {
            return nil
        }
        return (indexArray! as NSArray) as? Array<String>
    }
    
    func tableView(_ tableView: UITableView, didSelectRowAt indexPath: IndexPath) {
        
        tableView.deselectRow(at: indexPath as IndexPath, animated: true)
        let friend = groupFriends[indexPath.section][indexPath.row]
        let scfriend = SCFriend()
        scfriend.friendId = NSNumber(value: friend.friendId)
        scfriend.friendName = friend.friendName
        scfriend.avatar = friend.avatar
        
    }
    
    func tableView(_ tableView: UITableView, canFocusRowAt indexPath: IndexPath) -> Bool {
        return true
    }
    
    func tableView(_ tableView: UITableView, commit editingStyle: UITableViewCellEditingStyle, forRowAt indexPath: IndexPath) {
        if editingStyle == UITableViewCellEditingStyle.delete {
            let cell = tableView.cellForRow(at: indexPath as IndexPath) as! STFriendViewCell
            SCFriend.sharedInstance().deleteUserId(cell.user?.friendId, success: { () -> Void in
                STStorage.sharedInstance().delete(cell.user!)
            }, failure: { (code, msg) -> Void in
                iToast.makeText(msg).show()
            })
        }
    }
    
    func tableView(_ tableView: UITableView, editingStyleForRowAt indexPath: IndexPath) -> UITableViewCellEditingStyle {
        return UITableViewCellEditingStyle.delete
    }
}


//搜索控件的约束条件
extension FriendListViewController {
    
    private func getFetchedResultsController() -> NSFetchedResultsController<NSFetchRequestResult> {
        if fetchedResultsController != nil {
            return fetchedResultsController!
        }
        
        listFriends = Friend.mr_findAllSorted(by: "friendName", ascending: true) as! [Friend]
        fetchedResultsController = Friend.mr_fetchAllSorted(by: "friendName", ascending: true, with: nil, groupBy: nil, delegate: self)
        return fetchedResultsController!
    }
    
    func filterContentForSearchBarText(_ searchText: NSString) {
        listFriends = (Friend.mr_findAllSorted(by: "friendName", ascending: true) ) as! [Friend]
        let count = listFriends.count
        if searchText.length == 0 {
            theSearchBar?.placeholder = "FRIEND_COUNT".local() + "\(count)" + "PERSON".local()
            if count == 0 {
                theSearchBar?.placeholder = "NO_USER".local()
                tableView?.isHidden = true
                labelNoSouSuo?.isHidden = false
                
                return
            } else {
                tableView?.isHidden = false
                labelNoSouSuo?.isHidden = true
                
                let arrLast = NSMutableArray()
                
                for friend in listFriends {
                    let friendName = friend.friendName
                    if friendName != nil {
                        arrLast.add(friendName)
                    }
                }
                indexArray = STChineseString.indexArray(arrLast as [AnyObject])
                letterResultArr = STChineseString.letterSortArray(arrLast as [AnyObject])
            }
        } else {
            if count == 0 {
                tableView?.isHidden = true
                labelNoSouSuo?.isHidden = false
                
                return
            } else {
                tableView?.isHidden = false
                labelNoSouSuo?.isHidden = true
                listFriends = STChineseString.retrieveSortedListFriends(listFriends, by: searchText as String) as! [Friend]
                
                let arrLast = NSMutableArray()
                let friends: [Friend] = listFriends
                for friend in friends {
                    let friendName = friend.friendName
                    if friendName != nil {
                        arrLast.add(friendName)
                    }
                }
                indexArray = STChineseString.indexArray(arrLast as [AnyObject])
                letterResultArr = STChineseString.letterSortArray(arrLast as [AnyObject])
            }
        }
        
        groupFriends = STChineseString.reSortedListFriends(listFriends, byLetterSortArray: letterResultArr as! [Any] ) as! [[Friend]]
        tableView?.reloadData()
    }
}


//界面刷新好友列表，更新数据
extension FriendListViewController {
    
    func refreshNotice() {
        SCFriend.sharedInstance().requestList({ (result) in
            let newFriends = result as [SCFriend]?
            // NSLog("%@", newFriends)
            if (newFriends?.isEmpty)! {
                self.navigationItem.rightBarButtonItem?.image = UIImage(named: "friend_add")
                self.navigationItem.rightBarButtonItem?.tintColor = MAIN_TEXT_COLOR
            } else {
                self.navigationItem.rightBarButtonItem?.image = UIImage(named: "friend_add_new")
                self.navigationItem.rightBarButtonItem?.tintColor = UIColor.red
                
            }
        }) { (code, msg) in
            self.navigationItem.rightBarButtonItem?.image = UIImage(named: "friend_add")
            self.navigationItem.rightBarButtonItem?.tintColor = MAIN_TEXT_COLOR
        }
    }
    
    fileprivate func reloadData() {
        let actionTime = STSettings.sharedInstance().friendListUpdateTime
        let friendListUpdateTime = Int(NSDate().timeIntervalSince1970)
        
        if actionTime > 0 {
            SCFriend.sharedInstance().actionList(actionTime as NSNumber, success: {(result) in
                guard let friends: [SCFriend] = result else { return }
                
                for friend in friends {
                    switch friend.action {
                    case "add":
                        STStorage.sharedInstance().addOrUpdate(friend)
                        break
                    case "delete":
                        STStorage.sharedInstance().delete(friend)
                        break
                    default:
                        break
                    }
                }
                STSettings.sharedInstance().friendListUpdateTime = friendListUpdateTime
                
            }, failure: { (code, msg) -> Void in
                iToast.makeText(msg).show()
            })
        } else {
            SCFriend.sharedInstance().friendList({ (result) in
                let friends = result as [SCFriend]?
                STStorage.sharedInstance().addOrUpdateFriends(friends)
                STSettings.sharedInstance().friendListUpdateTime = friendListUpdateTime
                
            }, failure: { (code, msg) -> Void in
                iToast.makeText(msg).show()
            })
        }
    }
    
    func controllerDidChangeContent(controller: NSFetchedResultsController<NSFetchRequestResult>) {
        filterContentForSearchBarText("")
    }
    
    @objc func homeMenu() {
        self.mm_drawerController.toggle(MMDrawerSide.left, animated: true, completion: nil)
        UIApplication.shared.keyWindow?.endEditing(true)
        theSearchBar?.resignFirstResponder()
    }
    
    @objc func addFriend() {
        self.navigationController?.pushViewController(STAddFriendVC(), animated: true)
    }
    
    func searchBarCancelButtonClicked(_ searchBar: UISearchBar) {
        filterContentForSearchBarText((theSearchBar?.text)! as NSString)
    }
    
    func searchBarSearchButtonClicked(_ searchBar: UISearchBar) {
        filterContentForSearchBarText((theSearchBar?.text)! as NSString)
    }
    
    func searchBar(_ searchBar: UISearchBar, textDidChange searchText: String) {
        filterContentForSearchBarText(searchText as NSString)
    }
    
    func searchDisplayController(_ controller: UISearchDisplayController, shouldReloadTableForSearch searchString: String?) -> Bool {
        filterContentForSearchBarText(searchString! as NSString)
        return true
    }
    
    func searchBarShouldBeginEditing(_ searchBar: UISearchBar) -> Bool {
        return self.mm_drawerController.openSide == MMDrawerSide.none
    }
    
    func reloadFriendList(friend: SCFriend) {
        filterContentForSearchBarText((theSearchBar?.text)! as NSString)
    }
}
