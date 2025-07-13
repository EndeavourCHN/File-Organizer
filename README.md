# FileOrganizer

智能文件整理工具，支持按规则自动分类整理文件。

## 目录结构

```
FileOrganizer/
├── core/
│   ├── scanner.py
│   ├── classifier.py
│   └── organizer.py
├── config/
│   └── rules.yml
├── tests/
├── cli.py
└── README.md
```

## 使用方法

```bash
python cli.py <要整理的文件夹路径> [--size 100] [--no-large] [--no-temp]
```

- `--size` 超大文件门槛（MB），默认100
- `--no-large` 不清理超大文件
- `--no-temp` 不清理临时文件

## 规则配置

见 `config/rules.yml`，可自定义分类扩展名和临时文件扩展名。
