//
//  MTShareImageTableViewCell.swift
//  MYNT
//
//  Created by 李南君 on 2017/9/26.
//  Copyright © 2017年 slightech. All rights reserved.
//

import UIKit
import MYNTKit

class MTShareImageTableViewCell: MTBaseTableViewCell {
    
    @IBOutlet weak var nameLabel: UILabel!
    @IBOutlet weak var headImageView: UIImageView!
    @IBOutlet weak var shareToCancel: UIImageView!

    override func awakeFromNib() {
        super.awakeFromNib()
//        headImageView.layer.cornerRadius = headImageView.bounds.height / 2
    }
}

//    var didClickStopHandel: ((SCFriend) -> Void)?
//
//    weak var friend: SCFriend? {
//        didSet {
//            // TODO 更新头像名字
//            self.nameLabel.text = friend?.friendName
//            MKImageCache.shared.downUserAvatar(url: friend!.avatar) { image in
//            self.headImageView.layer.contents = image?.round()
//            }
//
//        }
//    }
