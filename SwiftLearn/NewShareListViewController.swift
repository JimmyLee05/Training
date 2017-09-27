//
//  NewShareListViewController.swift
//  MYNT
//
//  Created by 李南君 on 2017/9/26.
//  Copyright © 2017年 slightech. All rights reserved.
//

import UIKit
import MYNTKit

class NewShareListViewController: BaseViewController {

    @IBOutlet weak var tableview: UITableView!
    @IBOutlet weak var resultLabel: UILabel!
    @IBOutlet weak var addShareButton: UIButton!
    
    public class func show(parentViewController: UIViewController?, mynt: Mynt?) {
        let viewController  = NewShareListViewController()
        viewController.mynt = mynt
        parentViewController?.present(BaseNavigationController(rootViewController: viewController),
                                      animated: true,
                                      completion: nil)
    }
    
    var friends = [SCFriend]() {
        didSet {
            resultLabel.isHidden = !friends.isEmpty
            tableview.reloadData()
        }
    }
    
    override func viewDidLoad() {
        super.viewDidLoad()
        title = MTLocalizedString("已分享下列用户", comment: "已分享下列用户")
        setLeftBarButtonItem(image: Resource.Image.Navigation.close)
        
        addShareButton.backgroundColor          = ColorStyle.kBlueGradientColor.start
        addShareButton?.layer.cornerRadius      = addShareButton!.bounds.height / 2
        addShareButton.setTitle(MTLocalizedString("添加", comment: "添加"), for: .normal)
        
        tableview.register(with: MTShareImageTableViewCell.self)
        tableview.tableHeaderView   = UIView(frame: CGRect(x: 0, y: 0, width: winSize.width, height: 0))
        tableview.delegate          = self
        tableview.dataSource        = self
        
        resultLabel.text            = MTLocalizedString("GPS_ADD_RESULT", comment: "搜索结果")
        resultLabel.isHidden        = true
        
        tableview.reloadData()
        
        reloadFriendList()
    }
    
    override func didReceiveMemoryWarning() {
        super.didReceiveMemoryWarning()
    }
    
    override func leftBarButtonClickedHandler() {
        dismissNavigationController(animated: true, completion: nil)
    }
    
    @IBAction func didClickAddShareButton(_ sender: Any) {
        let viewController                          = SearchUsersViewController()
        viewController.mynt                         = mynt
        viewController.existFriends                 = friends
        viewController.shareFriendSuccessHandler    = { [weak self] in
            self?.reloadFriendList()
        }
        present(BaseNavigationController(rootViewController: viewController),
                animated: true,
                completion: nil)
    }
    // 重新加载用户列表
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
    
}

extension NewShareListViewController: UITableViewDelegate, UITableViewDataSource {
    
    func tableView(_ tableView: UITableView, numberOfRowsInSection section: Int) -> Int {
        return  friends.count
    }
    
    func tableView(_ tableView: UITableView, heightForRowAt indexPath: IndexPath) -> CGFloat {
        return 68
    }
    
    func tableView(_ tableView: UITableView, cellForRowAt indexPath: IndexPath) -> UITableViewCell {
        
        let friend  = friends[indexPath.row]
        let cell = tableView.dequeueReusableCell(cell: MTShareImageTableViewCell.self, for: indexPath)
        // 头像
        cell?.nameLabel.text = friend.friendName
        MKImageCache.shared.downUserAvatar(url: friend.avatar) { image in
            cell?.headImageView.image = image?.round()
        }
        return cell!
    }
    
//    func tableView(_ tableView: UITableView, didSelectRowAt indexPath: IndexPath) {
//        // Are you sure you want to share the MYNT GPS %name to %userName?\n\nThis user may watch the location and get the notification for this device.
//        let friend = friends[indexPath.row]
//        guard let mynt = mynt else { return }
//
//        let title   = MTLocalizedString("GPS_DIALOG_SURE", comment: "")
//        let message = MTLocalizedString("GPS_DIALOG_MESSAGE", comment: "")
//        let button  =  MTLocalizedString("GPS_DIALOG_YES", comment: "")
//        // 对话框
//        DialogManager.shared.show(title: title,
//                                  message: message,
//                                  buttonString: button,
//                                  image: UIImage(named: "dialog_reminder"),
//                                  clickOkHandler: { [weak self] _ in
//                                    // 开始分享
//                                    self?.shareFriends(friend: friend)
//        })
//    }
}