import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from tkcalendar import DateEntry
import secrets
import string
from datetime import datetime

class AdvancedKeyGenerator:
    def __init__(self, root):
        self.root = root
        self.root.title("高级密钥生成器 v2.0")
        self.root.geometry("950x700")
        
        # 初始化配置
        self.char_sets = {
            "uppercase": string.ascii_uppercase,
            "numbers": string.digits
        }
        self.excluded_chars = {'O', '0', 'I', '1', 'L', 'S', '5', 'Z', '2'}
        self.generated_keys = set()
        
        # 创建界面
        self.create_widgets()
        self.setup_style()
        
    def setup_style(self):
        """配置界面样式"""
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('TButton', padding=6)
        style.configure('TCheckbutton', font=('微软雅黑', 10))
        
    def create_widgets(self):
        """创建界面组件"""
        main_frame = ttk.Frame(self.root, padding=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # 控制面板
        control_frame = ttk.LabelFrame(main_frame, text="生成设置", padding=15)
        control_frame.pack(fill=tk.X, pady=5)
        
        # 第一行：数量设置
        quantity_frame = ttk.Frame(control_frame)
        quantity_frame.grid(row=0, column=0, sticky=tk.W, pady=5)
        
        ttk.Label(quantity_frame, text="生成数量:").pack(side=tk.LEFT)
        self.quantity = tk.IntVar(value=100)
        self.spin_quantity = ttk.Spinbox(
            quantity_frame,
            from_=1,
            to=10000,
            textvariable=self.quantity,
            width=8,
            validate="key",
            validatecommand=(self.root.register(self.validate_number), '%P')
        )
        self.spin_quantity.pack(side=tk.LEFT, padx=5)
        
        # 第二行：字符设置
        char_frame = ttk.Frame(control_frame)
        char_frame.grid(row=1, column=0, sticky=tk.W, pady=5)
        
        self.uppercase_var = tk.BooleanVar(value=True)
        self.numbers_var = tk.BooleanVar(value=True)
        self.exclude_similar_var = tk.BooleanVar()
        
        ttk.Checkbutton(char_frame, 
                       text="大写字母 (A-Z)", 
                       variable=self.uppercase_var).pack(side=tk.LEFT, padx=10)
        ttk.Checkbutton(char_frame, 
                       text="数字 (0-9)", 
                       variable=self.numbers_var).pack(side=tk.LEFT, padx=10)
        ttk.Checkbutton(char_frame,
                       text="排除相似字符 (0/O/1/I等)",
                       variable=self.exclude_similar_var).pack(side=tk.LEFT, padx=10)
        
        # 第三行：有效期设置
        expiry_frame = ttk.Frame(control_frame)
        expiry_frame.grid(row=2, column=0, sticky=tk.W, pady=5)
        
        ttk.Label(expiry_frame, text="有效期至:").pack(side=tk.LEFT)
        self.expiry_date = DateEntry(
            expiry_frame,
            date_pattern='yyyy-mm-dd',
            width=12,
            mindate=datetime.now()
        )
        self.expiry_date.pack(side=tk.LEFT, padx=5)
        
        # 生成按钮
        generate_btn = ttk.Button(control_frame, 
                                 text="生成密钥", 
                                 command=self.generate_keys,
                                 style='Accent.TButton')
        generate_btn.grid(row=3, column=0, pady=10, sticky=tk.EW)
        
        # 结果区域
        result_frame = ttk.LabelFrame(main_frame, text="生成的密钥", padding=15)
        result_frame.pack(fill=tk.BOTH, expand=True)
        
        self.text_area = tk.Text(
            result_frame, 
            wrap=tk.NONE, 
            font=('Consolas', 10), 
            height=20,
            padx=10,
            pady=10
        )
        
        vsb = ttk.Scrollbar(result_frame, orient="vertical", command=self.text_area.yview)
        hsb = ttk.Scrollbar(result_frame, orient="horizontal", command=self.text_area.xview)
        self.text_area.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
        
        self.text_area.grid(row=0, column=0, sticky="nsew")
        vsb.grid(row=0, column=1, sticky="ns")
        hsb.grid(row=1, column=0, sticky="ew")
        
        # 操作按钮
        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(pady=15)
        
        ttk.Button(btn_frame, 
                  text="全部复制", 
                  command=self.copy_all,
                  width=12).pack(side=tk.LEFT, padx=8)
        ttk.Button(btn_frame, 
                  text="导出文件", 
                  command=self.export_file,
                  width=12).pack(side=tk.LEFT, padx=8)
        ttk.Button(btn_frame,
                  text="清空记录",
                  command=self.clear_all,
                  width=12).pack(side=tk.LEFT, padx=8)
        
        # 布局配置
        result_frame.grid_rowconfigure(0, weight=1)
        result_frame.grid_columnconfigure(0, weight=1)
        control_frame.grid_columnconfigure(0, weight=1)
        
    def validate_number(self, value):
        """验证输入数量"""
        if value.isdigit() and 1 <= int(value) <= 10000:
            return True
        elif value == "":
            return True
        return False
        
    def get_filtered_chars(self):
        """获取过滤后的字符集"""
        chars = []
        if self.uppercase_var.get():
            chars.extend(self.char_sets["uppercase"])
        if self.numbers_var.get():
            chars.extend(self.char_sets["numbers"])
            
        if self.exclude_similar_var.get():
            chars = [c for c in chars if c not in self.excluded_chars]
            
        if not chars:
            messagebox.showerror("错误", "有效字符集为空，请修改设置")
            return None
        return chars
        
    def generate_single_key(self):
        """生成单个唯一密钥"""
        chars = self.get_filtered_chars()
        if not chars:
            return None
            
        max_retry = 1000
        for _ in range(max_retry):
            # 使用密码学安全随机数生成
            key = '-'.join(
                [''.join(secrets.choice(chars) for _ in range(5)) 
                for _ in range(5)]
            )
            if key not in self.generated_keys:
                self.generated_keys.add(key)
                return key
        raise RuntimeError("无法生成唯一密钥，请调整生成设置")
        
    def generate_keys(self):
        """批量生成密钥"""
        # 输入验证
        try:
            quantity = self.quantity.get()
            if quantity < 1 or quantity > 10000:
                raise ValueError
        except:
            messagebox.showerror("错误", "请输入1-10000之间的有效数量")
            return
            
        if not (self.uppercase_var.get() or self.numbers_var.get()):
            messagebox.showerror("错误", "请至少选择一种字符类型")
            return
            
        # 清空旧数据
        self.text_area.delete(1.0, tk.END)
        self.generated_keys.clear()
        
        # 生成密钥
        progress = ttk.Progressbar(self.root, mode='determinate', maximum=quantity)
        progress.place(x=20, y=650, width=910)
        
        try:
            keys = []
            for i in range(quantity):
                key = self.generate_single_key()
                if not key:
                    return
                keys.append(key)
                progress['value'] = i+1
                self.root.update_idletasks()
                
            self.text_area.insert(tk.END, '\n'.join(keys))
            messagebox.showinfo("完成", f"成功生成 {quantity} 个唯一密钥")
        except RuntimeError as e:
            messagebox.showerror("错误", str(e))
        finally:
            progress.destroy()
            
    def copy_all(self):
        """复制全部密钥"""
        content = self.text_area.get(1.0, tk.END).strip()
        if content:
            self.root.clipboard_clear()
            self.root.clipboard_append(content)
            messagebox.showinfo("成功", "已复制所有密钥到剪贴板")
            
    def export_file(self):
        """导出文件"""
        content = self.text_area.get(1.0, tk.END).strip()
        if not content:
            return
            
        # 添加元数据
        expiry_date = self.expiry_date.get_date().strftime("%Y-%m-%d")
        header = (
            f"# 密钥生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
            f"# 有效期至: {expiry_date}\n"
            f"# 生成数量: {len(content.splitlines())}\n\n"
        )
        full_content = header + content
        
        file_path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[
                ("文本文件", "*.txt"),
                ("CSV文件", "*.csv"),
                ("所有文件", "*.*")
            ],
            title="保存密钥文件"
        )
        
        if file_path:
            try:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(full_content)
                messagebox.showinfo("成功", f"文件已保存到：\n{file_path}")
            except Exception as e:
                messagebox.showerror("错误", f"保存失败：{str(e)}")
                
    def clear_all(self):
        """清空所有内容"""
        self.text_area.delete(1.0, tk.END)
        self.generated_keys.clear()
        messagebox.showinfo("提示", "已清空所有生成记录")

if __name__ == "__main__":
    try:
        from ttkthemes import ThemedTk
        root = ThemedTk(theme="arc")
    except ImportError:
        root = tk.Tk()
        
    # 设置窗口图标
    try:
        root.iconbitmap('key_icon.ico')
    except:
        pass
        
    app = AdvancedKeyGenerator(root)
    root.mainloop()