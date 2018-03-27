//
//  GlobalConst.swift
//  bbb
//
//  Created by bb on 16/8/5.
//  Copyright © 2016年 bb. All rights reserved.
//


import UIKit
import SVProgressHUD

let WIN_WIDTH = UIScreen.main.bounds.size.width
let WIN_HEIGHT = UIScreen.main.bounds.size.height
let MainColor = UIColor.init(red: 49/255, green: 194/255, blue: 124/255, alpha: 1)
let MainColor_HightLight = UIColor.init(red: 49/255, green: 194/255, blue: 124/255, alpha: 0.8)
let SeparatorColor = UIColor.init(red: 230/255, green: 230/255, blue: 230/255, alpha: 1)
let TitleColor = UIColor.init(red: 51/255, green: 51/255, blue: 51/255, alpha: 1)
let SubTitleColor = UIColor.darkGray
let detailTextColor = UIColor.init(red: 142/255, green: 142/255, blue: 147/255, alpha: 1)

let imageMainColor = creatImageWithColor(color: MainColor)
let imageHightLight = creatImageWithColor(color: MainColor_HightLight)
let imageDisabled = creatImageWithColor(color: MainColor_HightLight)
let imageOpacityNavigationBar = creatImageWithColor(color: UIColor.init(red: 255/255, green: 255/255, blue: 255/255, alpha: 0.5))

let pauseColor = UIColor.init(red: 221/255, green: 221/255, blue: 221/255, alpha: 1)
let pauseImage = creatImageWithColor(color: pauseColor)
let stopColor = UIColor.init(red: 243/255, green: 82/255, blue: 82/255, alpha: 1)
let stopImage = creatImageWithColor(color: stopColor)


//创建文件管理器
var fileManager = FileManager.default

//SVGProgressHUD二次 简易封装
func showProgressHUD(title:String){
    SVProgressHUD.show(withStatus: title)
    SVProgressHUD.dismiss(withDelay: 0.5)
    // 整个后面的背景选择
    SVProgressHUD.setDefaultMaskType(.none)
    // 弹出框颜色
    SVProgressHUD.setBackgroundColor(UIColor.init(red: 238/255, green: 238/255, blue: 238/255, alpha: 0.8))
    // 弹出框内容颜色
    SVProgressHUD.setForegroundColor(TitleColor)
    // 设置对应图片
    SVProgressHUD.setInfoImage(UIImage(named: "demo6")!)
    //字体
    SVProgressHUD.setFont(UIFont.systemFont(ofSize: 16))
    // 转圈的宽度
    SVProgressHUD.setRingThickness(2)
    // 位置 偏移
    SVProgressHUD.setOffsetFromCenter(UIOffset(horizontal: 0, vertical: 100))
}


//UIAlertController简易封装
func AlertController(title:String,message:String,ok:String,cancel:String,customAction:@escaping ()->()) ->UIAlertController{
    let alertController = UIAlertController(title: title, message: message, preferredStyle: .alert)
    let cancelAction = UIAlertAction(title: cancel, style: .cancel, handler: nil)
    let okAction = UIAlertAction(title: ok, style: .default, handler: {
        action in
        customAction()
    })
    alertController.addAction(cancelAction)
    alertController.addAction(okAction)
    return alertController
}


//把颜色直接换换成图片
func creatImageWithColor(color:UIColor) -> UIImage{
    let rect = CGRect(x: 0, y: 0, width: 1, height: 1)
    UIGraphicsBeginImageContext(rect.size)
    let context = UIGraphicsGetCurrentContext()
    context!.setFillColor(color.cgColor)
    context!.fill(rect)
    let image = UIGraphicsGetImageFromCurrentImageContext()
    UIGraphicsEndImageContext()
    return image!
}



//图片缩放方法(避免失真)
func scaleToSize(img:UIImage, size:CGSize) -> UIImage{
    UIGraphicsBeginImageContextWithOptions(size, false, 0.0)
    img.draw(in: CGRect(x: 0, y: 0, width: size.width, height: size.height))
    let scaledImage:UIImage = UIGraphicsGetImageFromCurrentImageContext()!
    UIGraphicsEndImageContext()
    return scaledImage
}


//富文本
func diverseStringOriginalStr(original : String,conversionStr conversion : String,withFont font :UIFont,withColor color : UIColor) ->NSMutableAttributedString{
    let range : NSRange = (original as NSString).range(of: conversion as String)
    let str = NSMutableAttributedString(string: original as String)
    str.addAttribute(NSAttributedStringKey.foregroundColor, value: color, range: range)
    str.addAttribute(NSAttributedStringKey.font, value: font, range: range)
    return str
}


