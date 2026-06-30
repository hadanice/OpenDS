#Q5 content
from typing import List, Optional

class TreeNode:
    def __init__(self, val: int):
        self.val = val
        self.left: Optional['TreeNode'] = None
        self.right: Optional['TreeNode'] = None

def build_tree(preorder: List[int], inorder: List[int]) -> Optional[TreeNode]:
    if not preorder:
        return None
    root_val = preorder[0]
    root = TreeNode(root_val)
    idx = inorder.index(root_val)          # 根在中序中的位置
    left_in = inorder[:idx]                # 左子树中序
    right_in = inorder[idx+1:]             # 右子树中序
    left_size = len(left_in)
    left_pre = preorder[1:1+left_size]     # 左子树先序
    right_pre = preorder[1+left_size:]     # 右子树先序
    root.left = build_tree(left_pre, left_in)
    root.right = build_tree(right_pre, right_in)
    return root


#Q6 content
def insertion_sort(a):
    for i in range(1,len(a)):
        j=i-1
        key=a[i]
        while j>0 and a[j]>key:
            a[j+1]=a[j]
            j-=1
        a[j+1]=key
    return a


#Q7 content
def merge(k,*args):
    if k == 1:
        return args[0]
    elif k == 2:
        i=j=0
        a1,a2=args[0],args[1]
        merged=[]
        while i<len(a1) and j<len(a2):
            if a1[i]<a2[j]:
                merged.append(a1[i])
                i+=1
            else:
                merged.append(a2[j])
                j+=1
        merged+=a1[i:]
        merged+=a2[j:]
        return merged
    else:
        half=k//2
        a1=merge(half,*args[:half])
        a2=merge(k-half,*args[half:])
        return merge(2,a1, a2)


#Q8 content
def well_merge(a,b):
        i=j=0
        c=[]
        while i<len(a) and j<len(b):
            if a[i]<b[j]:
                c.append(a[i])
                i+=1
            else:
                c.append(b[j])
                j+=1
        if i<len(a):
            c.extend(a[i:])
        if j<len(b):
            c.extend(b[j:])

        j=count=0
        for i in range(len(a)):
            while j<len(b) and a[i]>b[j]:
                j+=1
            count+=j
        return c,count

def do_well(a):
        if len(a) <= 1:
            return a,0
        mid=len(a) // 2
        a1,s1=do_well(a[:mid])
        a2,s2=do_well(a[mid:])
        a3,s3=well_merge(a1, a2)
        return a3,s1+s2+s3