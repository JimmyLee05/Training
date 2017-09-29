import UIKit

class ShareListTableViewCell: UITableViewCell {

    @IBOutlet weak var headImageView: UIImageView!
    @IBOutlet weak var nameLabel: UILabel!
    @IBOutlet weak var deleteButton: UIButton!
    
    weak var friend: SCFriend? {
        didSet {
            guard let friend = friend else { return }
            // 加载头像
            MKImageCache.shared.downUserAvatar(url: friend.avatar) { image in
                self.headImageView.layer.contents =  image?.round()?.cgImage
            }
            // 加载用户名
            nameLabel.text = friend.friendName
        }
    }
    
    // 点击删除按钮闭包
    var deleteButtonClickHandle: ((SCFriend?) -> Void)?
    
    override func awakeFromNib() {
        super.awakeFromNib()
        
    }
    
    override func setSelected(_ selected: Bool, animated: Bool) {
        super.setSelected(selected, animated: animated)

        // Configure the view for the selected state
    }
    
    @IBAction func didClickDeletaButton(_ sender: Any) {
        deleteButtonClickHandle?(friend)
    }
}