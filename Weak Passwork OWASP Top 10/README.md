# Top 10 OWASP 2017 Research
## Broken Authentication and Session Management
Đây là lỗ hổng bảo mật ứng dụng Web phổ biến đứng thứ 2 trong bảng xếp hạng OWASP Top 10 vào năm 2017. Khi các chức năng của ứng dụng triển khai không chính xác, kẻ tấn công có thể dễ dàng xâm nhập, ăn cắp thông tin tài khoản, mật khẩu và lợi dụng thông tin đã đánh cắp làm bàn đạp để khai thác các lỗ hổng khác. Đây có vẻ là lỗ hổng đơn giản nhưng nhiều người rất chủ quan nên dẫn đến kẻ tấn công có cơ hội khai thác dễ dàng.

Trong bài viết này mình chỉ giới thiệu 2 loại test case phổ biến cho đến nay vẫn tồn tại khá nhiều trên các ứng dụng Web:
- **[1. Default Credentials](#1-default-credentials)** - Mật khẩu mặc định
- **[2. Weak Password Policy](#2-weak-password-policy)** - Chính sách mật khẩu yếu

---
## 1. Default Credentials
### Reason
Lỗ hổng xuất hiện khi các ứng dụng sau khi cài đặt, không được cấu hình đúng cách hoặc sau khi tạo tài khoản người dùng, thông tin đăng nhập mặc định được cung cấp ban đầu không được thay đổi. Các thông tin đăng nhập mặc định này đã được các hãng sản xuất công khai trên Internet vì vậy kẻ tấn công có thể tìm kiếm dễ dàng.

### Practical
- Thông tin đăng nhập mặc định thường có độ dài khá ngắn và yếu để cho người dùng dễ nhớ chẳng hạn tên tài khoản sẽ là: "admin", "administrator", "root", "system", "guest", "test",... còn mật khẩu sẽ có dạng như là: "password", "123456", "pass123", "admin", "guest",... Đây chính là cơ hội để cho kẻ tấn công có thể dễ dàng đoán được mật khẩu của người dùng bằng cách thử đi thử lại nhiều lần cho đến khi đăng nhập thành công. Để tiết kiệm thời gian thì kẻ tấn công sử dụng các công cụ hay viết ra đoạn script để tự động hóa công việc đăng nhập.

<p align="center">
<img src="https://user-images.githubusercontent.com/38382423/221419030-7257ef3c-2740-41ab-a187-a4c51b60adaf.png" alt="burp-intruder-demo">
</p>

- Đối với tài khoản người dùng do người quản trị tạo và cấp hàng loạt thì sẽ có mật khẩu mặc định như nhau, dựa vào điều này kẻ tấn công có thể đăng nhập vào các tài khoản khác nhau với cùng một mật khẩu mặc định nếu họ chưa đổi.

- Đối với các nền tảng hay ứng dụng phổ biến, khi đã có được thông tin về phiên bản, model,... kẻ tấn công từ đó có thể tìm kiếm thông tin đăng nhập mặc định trong tài liệu hướng dẫn cài đặt hay đã được public trên Internet. Ví dụ thông tin đăng nhập của Apache Web Server có thể tìm thấy trên Google.

<p align="center">
<img src="https://user-images.githubusercontent.com/38382423/220574746-da3a330a-3825-414e-8e5c-9cb45e5eeb65.png" alt="apache-default-password">
</p>

---

## 2. Weak Password Policy
### Reason
Cơ chế xác thực phổ biến nhất hiện nay là mật khẩu. Mật khẩu đại diện cho chìa khóa của cả một vương quốc, nhưng thường người dùng lại không coi trọng vấn đề này. Thông thường các vụ tấn công xâm nhập vào hệ thống đều do người dùng bị lộ thông tin đăng nhập, điều đáng tiếc là hầu hết các mật khẩu phổ biến vẫn là: "123456", "password" và "qwerty",...

### Practical
- Người dùng hoặc người quản trị rất hay đặt thông tin đăng nhập theo tên của tổ chức họ đang làm việc, ví dụ ứng dụng có tên *Obscure* thì tài khoản và mật khẩu đăng nhập có thể là `obscure`/`obscure`. Dựa vào thông tin này, kẻ tấn công có thể dự đoán hoặc tạo ra danh sách mật khẩu kết hợp với chữ số hay kí tự đặc biệt như là "obscure@123", "0bscur3", "obscure123456",...

<p align="center">
<img src="https://github.com/Mebus/cupp/blob/master/screenshots/cupp-example.gif" alt="cupp-demo">
</p>

- Khi cơ chế xác thực cho phép người dùng có thể đăng nhập không giới hạn, kẻ tấn công có thể sử dụng kỹ thuật Brute-force để dò tên đăng nhập cũng như mật khẩu của bạn. Điều này càng nguy hiểm hơn nếu mật khẩu của bạn nằm trong danh sách [Top mật khẩu phổ biến trên thế giới](https://nordpass.com/most-common-passwords-list/).

<p align="center">
<img src="https://user-images.githubusercontent.com/38382423/222422016-13f9555f-5943-40e4-b6a4-425810200baf.png" alt="nordpass-top-password">
</p>

Đặc biệt mật khẩu của bạn càng dễ đoán và thời gian của kẻ tấn công tìm ra nhanh hơn nếu bạn đặt mật khẩu có ít hơn 8 kí tự và không bao gồm các kí tự đặc biệt, in hoa, số. Dưới đây là [trang web](https://www.passwordmonster.com/) có thể dự đoán mật khẩu của bạn có thể bị dò ra trong bao lâu.

<p align="center">
<img src="https://user-images.githubusercontent.com/38382423/222423332-fc75071c-c595-4f1c-8e69-71110ec523d6.png" alt="password-calculate">
</p>

---

## Mitigation
Để giảm thiểu lỗ hổng Broken Authentication cụ thể là các lỗi liên quan đến mật khẩu người dùng thì ta nên thực hiện các cách sau:
- **Multi-factor authentication**: Xác thực đa yếu tố gửi mã xác nhận OTP qua SMS, mail,...
- **Make strong password requirement**: Đặt mật khẩu mạnh hơn với độ dài ít nhất 8-12 kí tự gồm chữ thường, in hoa, số và kí tự đặc biệt. 
- **Limit failed login attempts**: Giới hạn số lần đăng nhập khi người dùng nhập sai quá bao nhiêu lần.
- **Change password regularly**: Thay đổi mật khẩu thường xuyên, tránh dùng mật khẩu cũ quá lâu.
- **Use credentials not related to your personal life**: Tránh việc đặt thông tin đăng nhập liên quan đến đời sống thường ngày của bạn.