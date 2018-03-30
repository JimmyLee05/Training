//
//  CoreDataManager.swift
//  Pomodoro Flow
//
//  Created by 李南君 on 2018/3/29.
//  Copyright © 2018年 Dan K. All rights reserved.
//

import UIKit
import CoreData

@available(iOS 10.0, *)
class CoreDataManager: NSObject {

    // 单例
    static let shared = CoreDataManager()

    // 拿到AppDelegate中创建好了的NSManagedObjectContext
    lazy var context: NSManagedObjectContext = {
        let context = ((UIApplication.shared.delegate) as! AppDelegate).context
        return context
    }()

    // 更新数据
    private func saveContext() {
        do {
            try context.save()
        } catch {
            let nserror = error as NSError
            fatalError("Unresolved error \(nserror), \(nserror.userInfo)")
        }
    }

    // 增加距离数据
    func saveDistance(distance: Double) {
        let run = NSEntityDescription.insertNewObject(forEntityName: "Run", into: context) as! Run
        run.distance = distance
        NSLog("distance------>\(run.distance)")
        saveContext()
    }

    // 获取所有数据
    func getAllRun() -> [Run] {
        let fetchRequest: NSFetchRequest = Run.fetchRequest()
        do {
            let result = try context.fetch(fetchRequest)
            return result
        } catch {
            fatalError();
        }
    }
}
