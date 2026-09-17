# 拿手好菜

家里的菜谱库。`recipes/` 里每道菜一个 Markdown 文件，`images/` 放成品图，`index.html` 是给手机用的选菜页面（由 `build.py` 生成）。

## 加一道菜

1. 在 `recipes/` 新建 `菜名.md`，格式照抄现有文件：

   ```
   # 菜名
   来源：[站名](链接)        （可选）
   标签：荤菜、快手           （可选值：自家拿手 荤菜 素菜 汤 主食 快手）
   用时：15分钟              （可选）

   一句话介绍。

   ## 成品图
   ![成品图](../images/菜名-成品.jpg)

   ## 材料（2人份）
   - 食材 用量

   ## 做法
   1. 步骤

   ## 小贴士
   ...
   ```

2. 成品图存为 `images/菜名-成品.jpg`。
3. 运行 `python3 build.py` 重新生成 `index.html`。

## 菜谱目录

- [麻辣厚揚洋葱回锅肉](recipes/麻辣厚揚洋葱回锅肉.md) — 自家拿手
- [小松菜炒蛋（麻油香）](recipes/小松菜炒蛋.md)
- [小炒西葫芦](recipes/小炒西葫芦.md)
- [牛肉炖萝卜](recipes/牛肉炖萝卜.md)
- [孜然土豆炒牛肉](recipes/孜然土豆炒牛肉.md)
- [干煸菜花（快手版）](recipes/干煸菜花（快手版）.md)
- [干煸菜花（五花肉版）](recipes/干煸菜花（五花肉版）.md)
- [西红柿鸡蛋汤](recipes/西红柿鸡蛋汤.md)
- [芹菜炒牛肉](recipes/芹菜炒牛肉.md)
- [羊肉炖白萝卜](recipes/羊肉炖白萝卜.md)
- [蒜蓉金针菇](recipes/蒜蓉金针菇.md)
- [芹菜家常豆腐](recipes/芹菜家常豆腐.md)
- [口蘑炒肉](recipes/口蘑炒肉.md)
- [豆豉蒸排骨](recipes/豆豉蒸排骨.md)
- [豇豆炒肉末](recipes/豇豆炒肉末.md)
- [蚝油杏鲍菇](recipes/蚝油杏鲍菇.md)
- [鸡蛋豆腐青菜汤](recipes/鸡蛋豆腐青菜汤.md)
- [青菜炒豆腐](recipes/青菜炒豆腐.md)
- [酸辣白菜](recipes/酸辣白菜.md)
- [土豆炖牛肉](recipes/土豆炖牛肉.md)
- [红烧蘑菇豆腐](recipes/红烧蘑菇豆腐.md)
- [蘑菇青菜粥](recipes/蘑菇青菜粥.md)
- [红烧肉](recipes/红烧肉.md)
