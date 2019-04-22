//
//  Status.swift
//  MCUClient
//
//  Created by Anatoly Kasyanov on 2/14/19.
//

import Foundation

class StatusAPI {

    let baseURL = "http://192.168.31.116"
//    let baseURL = "http://192.168.4.1"
   
    func makeGetCall(completion: @escaping (String) -> Void) {

        let statusEndpoint = baseURL

        // Set up the URL request
        guard let url = URL(string: statusEndpoint) else {
            print("Error: cannot create URL")
            return
        }
        let urlRequest = URLRequest(url: url)
        
        // set up the session
        let config = URLSessionConfiguration.default
        config.timeoutIntervalForRequest = 3
        
//        let session = URLSession(configuration: config)
        let session = URLSession(configuration: config)
        
        // make the request
        let task = session.dataTask(with: urlRequest) {
            (data, response, error) in
            // check for any errors
            guard error == nil else {
                completion("noConnection")
                print("error calling GET")
                print(error!)
                return
            }
            // make sure we got data    
            guard let responseData = data else {
                completion("noConnection")
                print("Error: did not receive data")
                return
            }
            // parse the result as JSON, since that's what the API provides
            do {
                guard let status = try JSONSerialization.jsonObject(with: responseData, options: [])
                    as? [String: Any] else {
                        completion("noConnection")
                        print("error trying to convert data to JSON")
                        return
                }
           
                // final result
                guard let isOpen = status["isOpen"] as? String else {
                    completion("noConnection")
                    print("Could not get isOpen key from JSON")
                    return
                }
                
                completion(isOpen)
                print("isOpen: \(isOpen)")

            } catch  {
                print("error trying to convert data to JSON")
                return
            }
        }
        task.resume()
    }
}
